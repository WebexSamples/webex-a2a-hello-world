# Webex A2A Hello World Server

A tiny Agent2Agent (A2A) server that beta testers can deploy when they do not already have an A2A endpoint for Webex Developer Portal testing.

This sample is intentionally boring: it exposes a public AgentCard and an echo-like "Hello World" skill over HTTPS after deployment. Use it to validate Agentic App registration and Control Hub provisioning only. Do not send customer data, secrets, or production traffic to this sample.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/WebexSamples/webex-a2a-hello-world)

## What This Deploys

- `GET /.well-known/agent-card.json` - A2A AgentCard discovery endpoint.
- `GET /.well-known/agent.json` - Compatibility alias for older A2A clients.
- `POST /` - JSON-RPC A2A endpoint.
- `GET /healthz` - Basic health check.

## Use In The Webex Developer Beta

1. Click **Deploy to Render**.
2. Approve the Render blueprint and wait for the service to deploy.
3. Open the generated `https://...onrender.com` service URL.
4. Confirm `/.well-known/agent-card.json` returns JSON.
5. In Webex Developer Portal, create a new Agentic App and select **A2A**.
6. Use the generated Render service URL as the **App URL**.

If you deploy somewhere other than Render, set `PUBLIC_URL` to the public HTTPS base URL for your service so the AgentCard advertises the correct endpoint.

## Run Locally

```bash
uv sync
uv run uvicorn webex_a2a_hello_world.app:app --host 0.0.0.0 --port 9999
```

Then open:

```text
http://127.0.0.1:9999/.well-known/agent-card.json
```

## Replit

You can import this GitHub repository into Replit and click **Run**. To publish it for Webex Developer Portal testing, use Replit's **Publish** flow and set `PUBLIC_URL` to the published `.replit.app` URL if the AgentCard does not already show that public URL.

## Attribution

This sample follows the official Agent2Agent hello-world sample shape from [`a2aproject/a2a-samples`](https://github.com/a2aproject/a2a-samples) and uses the official `a2a-sdk`.
