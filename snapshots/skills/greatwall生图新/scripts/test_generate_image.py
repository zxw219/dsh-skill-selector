"""离线验证：假密钥、模拟 HTTP 服务，不调用真实接口。"""

import base64
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from PIL import Image

import generate_image as gateway


REAL_CLIENT = httpx.Client
FAKE_KEY = "offline-test-key-only"


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="greatwall生图新-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        buffer = io.BytesIO()
        Image.new("RGB", (8, 8), (80, 100, 120)).save(buffer, format="PNG")
        self.png = buffer.getvalue()
        self.input_image = self.root / "参考图.png"
        self.input_image.write_bytes(self.png)
        self.out = self.root / "结果.png"
        self.requests = []

    def response(self, request):
        return httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(self.png).decode()}]})

    def run_script(self, mode="generate", extra=(), handler=None, key=FAKE_KEY):
        def capture(request):
            self.requests.append(request)
            return (handler or self.response)(request)

        def client(**kwargs):
            return REAL_CLIENT(transport=httpx.MockTransport(capture), **kwargs)

        args = [mode, "--model", "gpt-image-2.5-flare", "--prompt", "只展示服装正面", "--out", str(self.out), *extra]
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(gateway.httpx, "Client", side_effect=client), \
                patch.object(gateway, "get_env", return_value=key) as get_key, \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = gateway.main(args)
        self.assertNotIn(FAKE_KEY, stdout.getvalue() + stderr.getvalue())
        if get_key.called:
            get_key.assert_called_once_with("GATEWAY_IMAGE_NEW_API_KEY")
        output = stdout.getvalue() if code == 0 else stderr.getvalue()
        return code, json.loads(output)

    def test_all_four_models_are_sent_exactly(self):
        for model in gateway.SUPPORTED_MODELS:
            with self.subTest(model=model):
                self.out = self.root / (model + ".png")
                code, result = self.run_script(extra=("--model", model))
                self.assertEqual(code, 0)
                request = self.requests[-1]
                self.assertEqual(str(request.url), gateway.BASE_URL + "/images/generations")
                payload = json.loads(request.content)
                self.assertEqual(payload["model"], model)
                self.assertEqual(payload["n"], 1)
                self.assertEqual(payload["response_format"], "url")
                self.assertEqual(payload["quality"], "auto")
                self.assertNotIn("size", payload)
                self.assertEqual(request.headers["authorization"], "Bearer " + FAKE_KEY)
                self.assertTrue(result["ok"])
                with Image.open(result["path"]) as saved:
                    self.assertEqual(saved.format, "PNG")

    def test_model_is_required_and_removed_models_are_rejected(self):
        basic = ["generate", "--prompt", "服装", "--out", str(self.out)]
        rejected = ("unknown-model", "gpt-image-2", "gpt-image-2-exact", "gpt-image-2.5")
        for args in [basic, *(basic + ["--model", model] for model in rejected)]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    gateway.main(args)
                self.assertEqual(error.exception.code, 2)
        self.assertEqual(self.requests, [])

    def test_edit_uses_repeated_image_fields_and_mask(self):
        mask = self.root / "蒙版.png"
        Image.new("RGBA", (8, 8), (0, 0, 0, 0)).save(mask)
        code, _ = self.run_script("edit", ("--image", str(self.input_image), "--image", str(self.input_image), "--mask", str(mask)))
        self.assertEqual(code, 0)
        request = self.requests[0]
        self.assertEqual(str(request.url), gateway.BASE_URL + "/images/edits")
        self.assertTrue(request.headers["content-type"].startswith("multipart/form-data; boundary="))
        self.assertEqual(request.content.count(b'name="image";'), 2)
        self.assertNotIn(b'name="image[]"', request.content)
        self.assertIn(b'name="mask";', request.content)
        self.assertIn(self.png, request.content)
        self.assertIn("只展示服装正面".encode(), request.content)

    def test_url_is_downloaded_without_bearer_header(self):
        def handler(request):
            if request.method == "POST":
                return httpx.Response(200, json={"data": [{"url": "https://cdn.example.test/result.png"}]})
            self.assertNotIn("authorization", request.headers)
            return httpx.Response(200, content=self.png)

        code, _ = self.run_script(handler=handler)
        self.assertEqual(code, 0)
        self.assertEqual([request.method for request in self.requests], ["POST", "GET"])

    def test_prompt_file_size_and_response_format(self):
        prompt_file = self.root / "提示词.txt"
        prompt_file.write_text("完整中文提示词", encoding="utf-8-sig")
        def capture(request):
            self.requests.append(request)
            return self.response(request)

        args = ["generate", "--model", "gpt-image-2.5-flare", "--prompt-file", str(prompt_file),
                "--out", str(self.out), "--size", "1024x1536", "--quality", "high", "--response-format", "b64_json"]
        with patch.object(gateway.httpx, "Client", return_value=REAL_CLIENT(transport=httpx.MockTransport(capture))), \
                patch.object(gateway, "get_env", return_value=FAKE_KEY), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gateway.main(args), 0)
        payload = json.loads(self.requests[0].content)
        self.assertEqual(payload["prompt"], "完整中文提示词")
        self.assertEqual(payload["size"], "1024x1536")
        self.assertEqual(payload["quality"], "high")
        self.assertEqual(payload["response_format"], "b64_json")

    def test_existing_output_is_not_overwritten_or_submitted(self):
        self.out.write_bytes(b"original")
        code, _ = self.run_script()
        self.assertEqual(code, 1)
        self.assertEqual(self.requests, [])
        self.assertEqual(self.out.read_bytes(), b"original")

    def test_invalid_local_inputs_never_submit(self):
        broken = self.root / "损坏.png"
        broken.write_bytes(b"not an image")
        wrong_mask = self.root / "错误尺寸蒙版.png"
        Image.new("RGBA", (4, 4)).save(wrong_mask)
        cases = [("generate", ("--prompt", " ")), ("edit", ("--image", str(self.root / "missing.png"))),
                 ("edit", ("--image", str(broken))),
                 ("edit", ("--image", str(self.input_image), "--mask", str(wrong_mask)))]
        for mode, extra in cases:
            with self.subTest(mode=mode, extra=extra):
                code, _ = self.run_script(mode, extra)
                self.assertEqual(code, 1)
        self.assertEqual(self.requests, [])

    def test_mode_constraints(self):
        cases = [("edit", ()), ("generate", ("--image", str(self.input_image))),
                 ("generate", ("--mask", str(self.input_image)))]
        for mode, extra in cases:
            with self.subTest(mode=mode), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.run_script(mode, extra)
        self.assertEqual(self.requests, [])

    def test_missing_new_key_does_not_fall_back(self):
        code, result = self.run_script(key=None)
        self.assertEqual(code, 1)
        self.assertIn("GATEWAY_IMAGE_NEW_API_KEY", result["error"])
        self.assertEqual(self.requests, [])

    def test_http_errors_are_redacted_and_never_retried(self):
        for status in (400, 401, 403, 429, 500):
            with self.subTest(status=status):
                self.requests.clear()
                def handler(request):
                    return httpx.Response(status, json={"error": {"message": "rejected " + FAKE_KEY}})
                code, result = self.run_script(handler=handler)
                self.assertEqual(code, 1)
                self.assertEqual(len(self.requests), 1)
                self.assertIn("[REDACTED]", result["error"])
                self.assertFalse(result["generation_retried"])

    def test_generation_timeout_does_not_retry(self):
        def handler(request):
            raise httpx.ReadTimeout("simulated timeout", request=request)

        code, result = self.run_script(handler=handler)
        self.assertEqual(code, 1)
        self.assertEqual(len(self.requests), 1)
        self.assertIn("图片任务日志", result["error"])

    def test_failed_download_retains_link_without_regenerating(self):
        def handler(request):
            if request.method == "POST":
                return httpx.Response(200, json={"data": [{"url": "https://cdn.example.test/result.png"}]})
            return httpx.Response(410)

        code, result = self.run_script(handler=handler)
        self.assertEqual(code, 1)
        self.assertEqual(result["stage"], "download")
        self.assertEqual(result["image_url"], "https://cdn.example.test/result.png")
        self.assertEqual([request.method for request in self.requests], ["POST", "GET"])
        self.assertFalse(self.out.exists())

    def test_bad_remote_results_are_not_saved(self):
        items = [None, [], [{}], [{"b64_json": "%%%"}],
                 [{"b64_json": base64.b64encode(b"not image bytes").decode()}],
                 [{"url": "http://cdn.example.test/result.png"}]]
        for data in items:
            with self.subTest(data=data):
                self.requests.clear()
                code, _ = self.run_script(handler=lambda request: httpx.Response(200, json={"data": data}))
                self.assertEqual(code, 1)
                self.assertEqual(len(self.requests), 1)
                self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
