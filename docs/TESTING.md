## Testing Guide

### Quick Manual Tests
1) n8n UI: Manually execute HTTP Trigger with sample payload; verify OpenAI and Respond nodes succeed.
2) cURL/Webhook:
```bash
curl -X POST http://localhost:5678/webhook/ai-automation \
  -H "Content-Type: application/json" \
  -d '{"operation":"summarize","text":"n8n is a node-based automation tool.","targetLang":"en"}'
```
Expect HTTP 200 and JSON with `result`.
3) Streamlit: Run `streamlit run app.py`, fill form, confirm result renders.

### Negative Tests
- Missing `text`: expect error surfaced from Function node.
- Invalid `operation`: should fallback to summarize.
- Slow LLM: adjust timeout and confirm UI handles non-200 status gracefully.

### Regression Checklist
- Webhook path unchanged (`/ai-automation`).
- Respond node returns `result` field used by Streamlit.
- Model/provider changes keep response shape compatible or update Respond + Streamlit parsing.

