# scripts/test_prompt.py
import requests
import sys


def run_prompt_streaming(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
    }
    response = requests.post(
        "http://localhost:11434/api/generate", json=payload, stream=True
    )

    if response.status_code != 200:
        print("Error:", response.text)
        return

    print("📡 Streaming response:\n")
    for line in response.iter_lines():
        if line:
            try:
                print(eval(line.decode())["response"], end="", flush=True)
            except Exception as e:
                print(f"\nError decoding: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_prompt.py 'Your prompt here'")
        sys.exit(1)
    prompt = sys.argv[1]
    run_prompt_streaming("mistral", prompt)
