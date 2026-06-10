import os
from typing import Optional

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from google.protobuf.json_format import MessageToDict
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route

from webex_a2a_hello_world.agent_executor import HelloWorldAgentExecutor

DEFAULT_MAX_REQUEST_BYTES = 65_536


def _clean_base_url(value: str) -> str:
    return value.rstrip("/")


def _configured_base_url() -> Optional[str]:
    for key in (
        "PUBLIC_URL",
        "RENDER_EXTERNAL_URL",
        "REPLIT_DEPLOYMENT_URL",
        "REPLIT_DEV_DOMAIN",
    ):
        value = os.getenv(key)
        if value:
            if value.startswith("http://") or value.startswith("https://"):
                return _clean_base_url(value)
            return f"https://{_clean_base_url(value)}"
    return None


def _request_base_url(request: Request) -> str:
    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")
    if forwarded_proto and forwarded_host:
        return f"{forwarded_proto}://{forwarded_host}"
    return _clean_base_url(str(request.base_url))


def _max_request_bytes() -> int:
    value = os.getenv("MAX_REQUEST_BYTES")
    if not value:
        return DEFAULT_MAX_REQUEST_BYTES

    try:
        parsed = int(value)
    except ValueError:
        return DEFAULT_MAX_REQUEST_BYTES

    return parsed if parsed > 0 else DEFAULT_MAX_REQUEST_BYTES


class RequestGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > _max_request_bytes():
                return JSONResponse({"detail": "Request body too large."}, status_code=413)

        return await call_next(request)


def _make_agent_card(base_url: str) -> AgentCard:
    skill = AgentSkill(
        id="hello_world",
        name="Hello World",
        description="Acknowledges a text request and returns a harmless hello-world response.",
        input_modes=["text/plain"],
        output_modes=["text/plain"],
        tags=["a2a", "webex", "hello-world"],
        examples=["hello", "Say hello from my beta test"],
    )
    return AgentCard(
        name="Webex A2A Hello World",
        description=(
            "A minimal A2A sample server for Webex Developer testers who "
            "need a temporary endpoint for Agentic App registration."
        ),
        version="0.1.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        supported_interfaces=[
            AgentInterface(protocol_binding="JSONRPC", url=f"{_clean_base_url(base_url)}/")
        ],
        skills=[skill],
    )


def _agent_card_payload(base_url: str) -> dict:
    card = _make_agent_card(base_url)
    return MessageToDict(
        card,
        preserving_proto_field_name=False,
        always_print_fields_with_no_presence=False,
    )


async def homepage(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/.well-known/agent-card.json")


async def healthz(request: Request) -> JSONResponse:
    return JSONResponse({"ok": True})


async def agent_card(request: Request) -> JSONResponse:
    base_url = _configured_base_url() or _request_base_url(request)
    return JSONResponse(_agent_card_payload(base_url))


handler_card = _make_agent_card(_configured_base_url() or "http://127.0.0.1:9999")
request_handler = DefaultRequestHandler(
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=handler_card,
)

routes = [
    Route("/", homepage, methods=["GET"]),
    Route("/healthz", healthz, methods=["GET"]),
    Route("/.well-known/agent-card.json", agent_card, methods=["GET"]),
    Route("/.well-known/agent.json", agent_card, methods=["GET"]),
]
routes.extend(create_jsonrpc_routes(request_handler, "/"))

app = Starlette(routes=routes, middleware=[Middleware(RequestGuardMiddleware)])
