## Architecture Overview

### Components
- **n8n Workflow** (`ai-automation-workflow.json`): HTTP Trigger → Function (Prompt Prep) → OpenAI Chat → Respond to Webhook. Supports summarize, translate, reply, note.
- **LLM Provider**: OpenAI API (default `gpt-4o-mini`; configurable).
- **Streamlit Client** (`app.py`): Form-based UI that calls the n8n webhook.

### Data Flow
1) Client sends POST to `n8n /webhook/ai-automation` with JSON payload.  
2) Function node validates fields and builds task-specific prompt.  
3) OpenAI Chat node generates response.  
4) Respond to Webhook returns JSON `{ operation, result, model }` to client.  
5) Streamlit displays `result` and raw JSON for inspection.

### Extensibility Points
- Add notification nodes (Slack/Email/Discord) after OpenAI node.
- Insert RAG/vector search before OpenAI (Pinecone/Supabase/etc.) and append context to prompt.
- Swap model/provider by editing OpenAI node config or pointing to an OpenAI-compatible endpoint.

### Configuration Anchors
- Webhook path: `/webhook/ai-automation`
- Environment: `N8N_WEBHOOK_URL`, `N8N_TIMEOUT` (Streamlit), `OPENAI_API_KEY` (n8n credential).

