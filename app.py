import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv


# Load local .env if present (optional for webhook override)
load_dotenv()

DEFAULT_WEBHOOK = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/ai-automation")
DEFAULT_TIMEOUT = float(os.getenv("N8N_TIMEOUT", "20"))


def call_webhook(payload, url, timeout):
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}
    return resp.status_code, data


def main():
    st.set_page_config(page_title="n8n AI Automation Hub", page_icon="🤖", layout="wide")
    st.title("n8n AI Automation Hub")
    st.caption("摘要｜翻譯｜AI 回覆｜筆記整理 — 經由 n8n Webhook 呼叫")

    with st.sidebar:
        st.header("設定")
        webhook_url = st.text_input("Webhook URL", value=DEFAULT_WEBHOOK, help="例如 http://localhost:5678/webhook/ai-automation")
        timeout = st.number_input("Timeout (seconds)", min_value=5.0, max_value=120.0, value=DEFAULT_TIMEOUT, step=1.0)
        st.markdown("---")
        st.markdown("**操作提示**")
        st.markdown("- 確認 n8n workflow 已啟用並可透過上述 URL 存取。")
        st.markdown("- 必要環境變數：N8N_WEBHOOK_URL（選填）、N8N_TIMEOUT（選填）。")

    st.subheader("請求參數")
    col1, col2 = st.columns([2, 1])
    with col1:
        text = st.text_area("text（必要）", height=220, placeholder="貼上要摘要、翻譯或整理的文字")
    with col2:
        operation = st.selectbox("operation", options=["summarize", "translate", "reply", "note"], index=0)
        target_lang = st.text_input("targetLang", value="zh-TW", help="輸出語言，例如 en、zh-TW、ja...")
        style = st.text_input("style", value="concise", help="reply 時的口吻或風格")
        user = st.text_input("user", value="streamlit-user")

    payload = {
        "operation": operation,
        "text": text,
        "targetLang": target_lang,
        "style": style,
        "user": user,
    }

    if st.button("送出到 n8n"):
        if not text.strip():
            st.error("text 為必填")
            st.stop()

        with st.spinner("呼叫 n8n Webhook 中..."):
            try:
                status, data = call_webhook(payload, webhook_url, timeout)
                if 200 <= status < 300:
                    st.success(f"完成 (HTTP {status})")
                else:
                    st.warning(f"完成但回應碼 {status}")

                st.markdown("**結果內容**")
                if isinstance(data, dict) and "result" in data:
                    st.code(data.get("result", ""), language="markdown")
                else:
                    st.write(data)

                st.markdown("**原始回應 JSON**")
                st.code(json.dumps(data, ensure_ascii=False, indent=2))
            except requests.exceptions.RequestException as exc:
                st.error(f"請求失敗: {exc}")
            except Exception as exc:  # broad but ensures UI 回報
                st.error(f"處理回應時出錯: {exc}")

    st.markdown("---")
    st.markdown("若 Webhook URL 與回傳欄位不同，請在 sidebar 調整 URL，並於 n8n Respond 節點保持 `result` 欄位即可。")


if __name__ == "__main__":
    main()
