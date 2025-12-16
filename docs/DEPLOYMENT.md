## Deployment Guide

### Prerequisites
- Docker or Node runtime for n8n.
- OpenAI API key stored in n8n Credentials.
- Git access to `https://github.com/g114064160-rgb/AIOT-HW5-2`.

### n8n Setup (Docker one-liner)
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
- Open n8n UI → Credentials → OpenAI → 填入 API Key。
- Flows → Import → 上傳/貼上 `ai-automation-workflow.json` → Enable。

### Streamlit App
```bash
pip install -r requirements.txt
streamlit run app.py
```
- 可用 `.env` 或側欄調整 `N8N_WEBHOOK_URL`。

### Git Pull/Update
```bash
git clone https://github.com/g114064160-rgb/AIOT-HW5-2
cd AIOT-HW5-2
pip install -r requirements.txt
```

### Production Notes
- For long-running n8n, prefer docker-compose with volume mounts for persistence.
- If exposing publicly, place behind HTTPS reverse proxy and configure webhook URL accordingly.
- Configure model/temperature/token limits in OpenAI node to control cost.

