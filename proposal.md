## Proposal: n8n AI Automation Hub + Streamlit Client

### Goals
- 提供一套可運作的 n8n Workflow，支援摘要、翻譯、AI 回覆、筆記整理，透過 Webhook 對外服務。
- 建立 Streamlit 前端 `app.py`，方便以表單方式呼叫 Webhook，快速測試與展示。
- 預計推送至 GitHub repo: https://github.com/g114064160-rgb/AIOT-HW5-2

### Workflow 摘要
- 檔案：`ai-automation-workflow.json`
- 流程：HTTP Trigger (`/ai-automation`, POST) → Function (依 operation 組 prompt) → OpenAI Chat (預設 gpt-4o-mini) → Respond to Webhook。
- 支援 operation：`summarize`（預設）、`translate`、`reply`、`note`。
- 請在 OpenAI 節點替換 credential id 為你的 OpenAI 憑證。

### Streamlit App 設計（app.py）
- 目的：以表單呼叫 n8n Webhook，並顯示結果。
- 主要元素：
  - 輸入欄位：operation 選單、text（主要內容）、targetLang、style、user。
  - Sidebar 設定：Webhook URL（預設 `http://localhost:5678/webhook/ai-automation`），Request timeout。
  - 送出後，以 `requests` 對 Webhook POST JSON，顯示回傳 result 與原始回應 JSON。
  - 失敗時顯示錯誤訊息與 HTTP 狀態碼。
- 相依：`streamlit`、`requests`、`python-dotenv`（選用，若要從 .env 載入）。

### 安裝與執行
1) 準備 n8n
- 啟動 n8n（本地或雲端），匯入 `ai-automation-workflow.json`，啟用並設定 OpenAI Credentials。
- 確認 Webhook URL，例如本地預設 `http://localhost:5678/webhook/ai-automation`。

2) 啟動 Streamlit
```bash
pip install streamlit requests python-dotenv
streamlit run app.py
```
- 在 UI 填寫 text 及 operation，送出後應收到 JSON 回應。

### 推送到 GitHub（需本機已登入 git）
```bash
git init
git remote add origin https://github.com/g114064160-rgb/AIOT-HW5-2
git add .
git commit -m "Add n8n AI workflow, Streamlit client, and docs"
git push -u origin main   # 若預設分支為 master 請改 master
```
- 若需設定使用者資訊：`git config user.name "Your Name"`、`git config user.email "g114064160@smail.nchu.edu.tw"`。
