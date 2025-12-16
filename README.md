## n8n AI Automation Hub

這份 README 說明一套可立即運作的 n8n Workflow，涵蓋摘要、翻譯、AI 回覆、筆記整理與 Webhook 自動化。靈感來自影片 https://www.youtube.com/watch?v=aXocGiEx-qc 並依循專案 https://github.com/soluckysummer/n8n_workflows 的結構。

---

### 1) 專案簡介
- 目的：提供一個可透過 Webhook 呼叫的多功能 AI Hub，集中處理文字摘要、翻譯、客服式回覆與行動筆記整理。
- 核心節點：HTTP Trigger → Function (準備 Prompt) → OpenAI Chat → Respond to Webhook。
- 輸入：HTTP POST 傳入 text、operation 等欄位；輸出：JSON 包含 AI 結果。

### 2) 架構概覽
1. HTTP Trigger 監聽 `/ai-automation` 路徑並接收 POST 請求。
2. Function 節點依 operation 組合指令，產出適合的 Prompt。
3. OpenAI Chat 節點呼叫 LLM（預設 gpt-4o-mini）。
4. Respond to Webhook 回傳 JSON，包含 operation 與生成結果。

### 3) 先決條件
- n8n 版本：≥ 1.20（建議最新版）。
- 安裝方式：雲端、桌面版或 Docker 均可；本文件以 Docker compose 與本地 UI 匯入為例。
- 必要憑證：OpenAI API Key。
- 環境需求：Node 18+（若本機安裝）、Docker（若用 compose）、git（選擇性）。

### 4) 安裝與啟動
**Docker compose 啟動範例**
```bash
docker run -it --rm \
  -p 5678:5678 \
  -e N8N_HOST=localhost \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL=http \
  -e GENERIC_TIMEZONE="Asia/Taipei" \
  -e NODE_FUNCTION_ALLOW_BUILTIN=util \
  n8nio/n8n:latest
```
（或使用官方 docker-compose.yml，視需要掛載資料卷）

**匯入 workflow**
1. 進入 n8n UI → Flows → Import.
2. 貼上 `ai-automation-workflow.json` 內容或上傳檔案。
3. 儲存後啟用 Workflow。

**Streamlit 用戶端（選用）**
- 安裝依賴：`pip install -r requirements.txt`
- 啟動：`streamlit run app.py`
- 如需修改 Webhook URL，於 UI 側欄或 `.env`/`.env.example` 中設定 `N8N_WEBHOOK_URL`。

### 5) 環境變數與憑證設定
- 在 n8n Credentials → OpenAI API 建立憑證，填入 `OPENAI_API_KEY`。
- 若用 .env（供 Docker 或本機）：  
  ```env
  OPENAI_API_KEY=sk-xxxxx
  N8N_HOST=localhost
  N8N_PORT=5678
  N8N_PROTOCOL=http
  ```
- 將 workflow 中 OpenAI Chat 的 credential id 替換為你在 UI 建立的憑證。

### 6) 工作流詳解（節點）
- HTTP Trigger  
  - 方法：POST，路徑 `/ai-automation`，responseMode 設為 lastNode，以 Respond to Webhook 回傳。
- Prepare Prompt (Function)  
  - 驗證 `text`，允許的 operation：`summarize`、`translate`、`reply`、`note`。  
  - 根據 operation 組合任務指令，預設 targetLang=`en`，style=`concise`。  
  - 輸出：`prompt` 字串與 `meta`（operation、targetLang、style、user）。
- OpenAI Chat  
  - 模型：`gpt-4o-mini`（可改 gpt-4o/gpt-4.1 等）。  
  - 系統訊息：要求精準且節省 Token。  
  - user 訊息：使用 Function 生成的 prompt。  
  - 溫度 0.2，maxTokens 800，可依需求調整。
- Respond to Webhook  
  - 回傳 JSON：`operation`、`result`（取自 choices[0].message.content）、`model`。
  - 若 OpenAI 回傳欄位因版本不同，可在此節點調整表達式。

### 7) 觸發與請求格式
- HTTP/Webhook：`POST http://<your-host>:5678/webhook/ai-automation`
- 範例 body（application/json）：
```json
{
  "operation": "summarize",
  "text": "n8n 是一個基於節點的自動化平台，可用於編排 API、資料流與 AI。",
  "targetLang": "zh-TW",
  "style": "helpful",
  "user": "demo-user"
}
```
- operation 可用值：`summarize`（預設）、`translate`、`reply`、`note`。
- 回應示例：
```json
{
  "operation": "summarize",
  "result": "- n8n 是節點式自動化平台...\n- ...\nTL;DR: ...",
  "model": "gpt-4o-mini"
}
```

### 8) 資料來源 / 向量搜尋（若需擴充）
- 本 workflow 以即時輸入為主，未綁定向量庫。
- 若要加入 RAG，可在 Function 前後插入向量搜尋節點（如 Pinecone、Supabase、Weaviate），並將檢索到的 context 併入 prompt。

### 9) 輸出與通知
- 目前回傳 Webhook JSON。  
- 若要通知 Slack/Email/Discord，於 OpenAI 之後新增對應節點並使用 `{{$json["choices"][0]["message"]["content"]}}` 作為訊息本文。

### 10) 測試與除錯
- 在 n8n UI 手動執行 HTTP Trigger，輸入測試 body。
- 常見錯誤：
  - 401/429：OpenAI 金鑰錯誤或額度不足。
  - Webhook 404：確認 URL 路徑 `/webhook/ai-automation`，啟用後才可用。
  - 表達式 undefined：確認 OpenAI 節點輸出欄位名稱，必要時在 Respond 節點修改表達式。
- 日誌：Settings → Execution list 可查看每次執行紀錄與資料。

### 11) 版本控制與部署
- 檔案結構建議：  
  - `ai-automation-workflow.json`：主 workflow。  
  - `README.md`：文件與操作說明。  
  - `.env.example`（可自行建立）：列出必要環境變數。
- 部署：將 JSON 匯出後在目標環境 UI 匯入；或使用 n8n CLI API 匯入（若已啟用）。

### 12) 安全與合規
- API Key 勿 commit；使用 n8n Credentials 儲存。  
- 僅授權必要權限；敏感輸入可在 Function 節點過濾。  
- 控制成本：限制 maxTokens、設排程、避免高頻觸發。

### 13) 自訂與擴充
- 更換模型：在 OpenAI Chat 節點改成 gpt-4.1 / gpt-3.5-turbo 或本地 LLM（改用 OpenAI 兼容端點）。  
- 增加節點：可插入資料庫、Webhook、表單來源或 CRM 同步。  
- Prompt 調優：在 Function 內調整 style/targetLang；新增工具指令（如格式模板、JSON 輸出）。

### 14) 範例使用情境
- 客服回覆：operation=`reply`，接入表單或聊天 Webhook，AI 生成客服回應並推送 Slack。  
- 定時摘要：用 Cron 觸發外部資料抓取 → Function 整理 → OpenAI 摘要 → Email 通知。  
- 筆記整理：表單/Notion Webhook 將雜訊文字送入 → operation=`note` → 產出行動清單與截止時間。

### 15) 授權與參考
- 授權：依你專案需求設定（此文件未附帶特定授權）。  
- 參考來源：  
  - YouTube: https://www.youtube.com/watch?v=aXocGiEx-qc  
  - GitHub: https://github.com/soluckysummer/n8n_workflows  

---

立即匯入 `ai-automation-workflow.json`，設定 OpenAI 憑證，即可對外提供摘要、翻譯、AI 回覆、筆記整理等多合一 Webhook 服務。***
