## Security Guidelines

### Secrets Handling
- Store `OPENAI_API_KEY` in n8n Credentials, not in repo or env files committed.
- `.env` files are for local use; keep `.env.example` non-sensitive.

### Access Control
- Protect n8n UI with authentication and restrict network exposure (use reverse proxy + HTTPS).
- Limit who can trigger webhooks; if needed, add a shared secret header/token check in Function node.

### Data Handling
- Avoid logging sensitive user text; use n8n execution logs sparingly and purge when not needed.
- Apply least privilege to external services (email/chat/webhooks).

### Rate/Cost Control
- Set reasonable `maxTokens` and temperature in OpenAI node.
- Add throttling/rate-limit nodes or upstream gateway rules if exposed publicly.

