# ABTalks Agent Frontend

A lightweight frontend for the ABTalks autonomous AI-security backend.

## Run locally

Because this is plain HTML/CSS/JavaScript, no frontend build step is required.

1. Start the backend:

```powershell
uvicorn app.main:app --reload
```

2. Serve this folder with a local static server. For example:

```powershell
python -m http.server 5500
```

3. Open:

```text
http://127.0.0.1:5500
```

4. Keep the backend URL as:

```text
http://127.0.0.1:8000
```

## Backend endpoints used

- `POST /api/agent/init`
- `GET /api/agent/feed?agentId=<agentId>`

The frontend stores the returned agent ID in localStorage.

## Deployment

For a live deployment, set the Backend URL field to the public HTTPS URL of the deployed FastAPI backend.

Do not put Gemini or Breeth API keys in this frontend.
