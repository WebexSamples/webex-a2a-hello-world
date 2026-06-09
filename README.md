# Webex A2A Hello World Server

A tiny Agent2Agent (A2A) server that beta testers can deploy when they do not already have an A2A endpoint for Webex Developer Portal testing.

This sample is intentionally boring: it exposes a public AgentCard and an echo-like "Hello World" skill over HTTPS after deployment. Use it to validate Agentic App registration and Control Hub provisioning only. Do not send customer data, secrets, or production traffic to this sample.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&builder=buildpack&repository=github.com%2FWebexSamples%2Fwebex-a2a-hello-world&branch=main&name=webex-a2a-hello-world&ports=8000%3Bhttp%3B%2F&run_command=PYTHONPATH%3Dsrc%20uvicorn%20webex_a2a_hello_world.app%3Aapp%20--host%200.0.0.0%20--port%208000)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/WebexSamples/webex-a2a-hello-world)

## What This Deploys

- `GET /.well-known/agent-card.json` - A2A AgentCard discovery endpoint.
- `GET /.well-known/agent.json` - Compatibility alias for older A2A clients.
- `POST /` - JSON-RPC A2A endpoint.
- `GET /healthz` - Basic health check.

## Use In The Webex Developer Beta

1. Click **Deploy to Koyeb**.
2. Approve the deployment and wait for the service to deploy.
3. Open the generated public HTTPS service URL.
4. Confirm `/.well-known/agent-card.json` returns JSON.
5. In Webex Developer Portal, create a new Agentic App and select **A2A**.
6. Use the generated service URL as the **App URL**.

If your host does not forward its public hostname to the app, set `PUBLIC_URL` to the public HTTPS base URL for your service so the AgentCard advertises the correct endpoint.

## Free Hosting Options

- **Koyeb** is the recommended free path for this sample. It can deploy a Python web service/API from GitHub and exposes a public HTTPS URL.
- **Hugging Face Spaces** can also run this kind of small Python service on free CPU hardware, but it is less direct for a plain A2A API than Koyeb.
- **Replit** is useful for trying and editing the sample. Depending on your Replit plan, publishing a stable public app may require a paid deployment.
- **Render** may still show a free option in some accounts/workspaces, but use Koyeb first if Render asks for a paid plan.

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
