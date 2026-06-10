import unittest
from pathlib import Path

from starlette.testclient import TestClient

from webex_a2a_hello_world.app import app


class AppGuardrailTests(unittest.TestCase):
    def test_oversized_post_body_is_rejected(self) -> None:
        client = TestClient(app)

        response = client.post(
            "/",
            content=b"x" * 65_537,
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, 413)


class LambdaHandlerTests(unittest.TestCase):
    def test_lambda_handler_is_callable(self) -> None:
        from lambda_handler import handler

        self.assertTrue(callable(handler))


class SamTemplateTests(unittest.TestCase):
    def test_lambda_runtime_can_import_src_package(self) -> None:
        template = Path("template.yaml").read_text()

        self.assertIn("PYTHONPATH: /var/task/src", template)


if __name__ == "__main__":
    unittest.main()
