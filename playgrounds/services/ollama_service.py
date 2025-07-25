import requests
import time
import json


class OllamaService:
    BASE_URL = "http://localhost:11434/api/generate"

    @staticmethod
    def run_prompt(prompt_text, input_vars, stream=False):
        full_prompt = prompt_text.format(**input_vars)

        payload = {
            "model": "mistral",
            "prompt": full_prompt,
            "stream": stream,
        }

        start_time = time.time()

        if not stream:
            response = requests.post(OllamaService.BASE_URL, json=payload)
            latency_ms = int((time.time() - start_time) * 1000)

            if response.status_code != 200:
                raise ValueError("Failed to get response from Ollama")

            result = response.json()["response"]
            return {"result": result, "tokens_used": None, "latency_ms": latency_ms}

        # Stream True
        response = requests.post(OllamaService.BASE_URL, json=payload, stream=True)
        latency_ms = int((time.time() - start_time) * 1000)

        if response.status_code != 200:
            raise ValueError("Failed to get response from Ollama")

        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = line.decode("utf-8")
                    data = json.loads(chunk)
                    text = data.get("response", "")
                    print(text, end="", flush=True)
                    result += text
                except Exception as e:
                    print(f"\n[Streaming error]: {e}")

        return {"result": result, "tokens_used": None, "latency_ms": latency_ms}
