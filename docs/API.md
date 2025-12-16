## API Contract: n8n Webhook `/webhook/ai-automation`

### Request
- Method: `POST`
- URL: `http://<host>:5678/webhook/ai-automation`
- Headers: `Content-Type: application/json`
- Body (all strings):
  - `operation` (optional): `summarize` | `translate` | `reply` | `note` (default: `summarize`)
  - `text` (required): main content
  - `targetLang` (optional): output language (default: `en`)
  - `style` (optional): tone/style, mainly for `reply` (default: `concise`)
  - `user` (optional): caller id (default: `user`)

Example:
```json
{
  "operation": "translate",
  "text": "n8n 是一個自動化平台。",
  "targetLang": "en",
  "style": "helpful",
  "user": "demo-user"
}
```

### Response
- Status: `200 OK` on success
- Body:
```json
{
  "operation": "translate",
  "result": "<model-generated text>",
  "model": "gpt-4o-mini"
}
```

### Errors
- Missing text: HTTP 500 from Function node (validation error).
- Auth/Quota issues: HTTP 4xx/5xx from OpenAI; n8n returns error payload.
- URL/activation errors: HTTP 404 if workflow not active or path mismatch.

