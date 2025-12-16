## Operations & Runbook

### Health Checks
- n8n UI reachable on configured host/port (default `http://localhost:5678`).
- Webhook test: POST to `/webhook/ai-automation` with sample payload; expect HTTP 200 and `result`.
- Streamlit UI: load page, send test request, confirm response.

### Logs & Monitoring
- n8n: Settings → Execution list for run history and node-level data.
- Docker: `docker logs <container>` for runtime errors.
- Streamlit: console output; wrap `requests` exceptions handled in UI.

### Common Issues
- 401/429 from OpenAI: check API key validity/quotas.
- 404 webhook: ensure workflow is enabled and path is `/ai-automation`.
- Expression undefined: adjust Respond node to match OpenAI output shape.
- Timeouts: increase `N8N_TIMEOUT` for Streamlit or optimize prompt/max tokens.

### Maintenance
- Rotate API keys in n8n Credentials; avoid storing in repo.
- Backup: export workflow JSON periodically or mount n8n data volume in Docker.
- Updates: pull latest repo, re-import workflow if structure changed.

