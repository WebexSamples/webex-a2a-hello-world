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

## Low-Cost AWS Deployment

This repository includes an AWS SAM template for a low-cost Lambda Function URL deployment. The deployment uses:

- AWS Lambda with the ARM64 architecture, 128 MB memory, and a 5 second timeout.
- A public Lambda Function URL for HTTPS access from Webex Developer Portal.
- Reserved concurrency set to `2` by default to cap concurrent execution.
- `MAX_REQUEST_BYTES=65536` so oversized POST bodies are rejected with `413`.
- `IntendedPublic=true` on the Lambda function because this sample serves only public hello-world data.

Deploy with:

```bash
sam build --use-container
sam deploy \
  --stack-name webex-a2a-hello-world \
  --region us-east-1 \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --parameter-overrides \
    ReservedConcurrency=2 \
    FunctionTimeoutSeconds=5 \
    FunctionMemoryMb=128 \
    MaxRequestBytes=65536
```

Limit CloudWatch log retention after the first deployment:

```bash
aws logs put-retention-policy \
  --log-group-name /aws/lambda/webex-a2a-hello-world \
  --retention-in-days 7 \
  --region us-east-1
```

After deploy, copy the `FunctionUrl` output and confirm:

```bash
BASE_URL="${FUNCTION_URL%/}"
curl "$BASE_URL/.well-known/agent-card.json"
curl "$BASE_URL/healthz"
curl \
  -H "content-type: application/json" \
  -H "A2A-Version: 1.0" \
  --data '{"jsonrpc":"2.0","id":"1","method":"SendMessage","params":{"message":{"messageId":"test-message-1","role":"ROLE_USER","parts":[{"text":"hello"}]}}}' \
  "$BASE_URL/"
```

To remove the AWS resources when testing is done:

```bash
sam delete --stack-name webex-a2a-hello-world --region us-east-1
```

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
