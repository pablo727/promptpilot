#!/usr/bin/env python

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.token_utils import update_headers

import requests
import json
import readline  # enables arrow-key history
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv
import subprocess


console = Console()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

HEADERS = update_headers()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def refresh_token():
    print("🔁 Refreshing expired token...")
    result = subprocess.run(
        ["bash", "scripts/get_token.sh"], capture_output=True, text=True
    )
    print(result.stdout)

    # Force override of existing env vars
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=True
    )
    global HEADERS
    HEADERS = update_headers()


HISTORY_URL = "http://localhost:8000/api/v1/chatmessages/"
OLLAMA_URL = "http://localhost:11434/api/generate"


def get_chat_history():
    global HEADERS

    def do_get():
        return requests.get(HISTORY_URL, headers=HEADERS)

    try:
        response = do_get()
        if response.status_code == 401:
            console.print(
                "[yellow]Token expired or invalid, refreshing token...[/yellow]"
            )
            refresh_token()
            HEADERS = update_headers()
            response = do_get()  # retry once

        if response.status_code == 200:
            messages = response.json()
            console.print("\n[bold cyan]📜 Chat History:[/bold cyan]")
            for msg in reversed(messages[-10:]):  # Last 10 messages
                role = msg.get("role", "unknown")
                user = msg.get("user", "unknown")
                text = msg.get("message", "")
                console.print(f"[bold yellow]{role}[/bold yellow] ({user}): {text}")
        else:
            console.print(f"[red]Failed to fetch history: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error fetching history: {e}[/red]")


def post_chat_message(role, message, username="admin"):
    global HEADERS
    payload = {
        "role": role,
        "username": username,
        "message": message,
    }

    def do_post():
        return requests.post(HISTORY_URL, json=payload, headers=HEADERS)

    try:
        response = do_post()
        if response.status_code == 401:
            console.print(
                "[yellow]Token expired or invalid, refreshing token...[/yellow]"
            )
            refresh_token()
            HEADERS = update_headers()
            response = do_post()  # retry once

        if response.status_code not in {200, 201}:
            console.print(
                f"[red]❌ Failed to save message: {response.status_code}[/red]"
            )
            console.print(f"[red]{response.text}[/red]")

    except Exception as e:
        console.print(f"[red]❌ Error saving message: {e}[/red]")


def chat_with_ollama(model="mistral"):
    console.print(
        "[bold green]🤖 Welcome to Ollama Chat CLI! Type 'exit' to quit.[/bold green]\n"
    )

    # Force override of existing env vars
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), "..", "env"), override=True
    )
    global HEADERS
    HEADERS = update_headers()

    while True:
        try:
            user_input = input("🟢 Input: ")
            if user_input.lower() in {"exit", "quit"}:
                console.print("[bold red]Exiting...[/bold red]")
                break
            elif user_input.lower() == "/history":
                get_chat_history()
                continue

            # Save user's message
            post_chat_message("user", user_input, username="admin")

            # Stream response from Ollama

            payload = {
                "model": model,
                "prompt": user_input,
                "stream": True,
            }

            print("📦 Payload:", json.dumps(payload, indent=2))

            response = requests.post(
                "http://localhost:11434/api/generate", json=payload, stream=True
            )

            if response.status_code != 200:
                console.print(f"[red]❌ Error: {response.text}[/red]")
                continue

            console.print("[bold cyan]🤖 Mistral:[/bold cyan] ", end="")
            result = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode())
                        text = chunk.get("response", "")
                        print(text, end="", flush=True)
                        result += text
                    except Exception as e:
                        console.print(f"\n[red]Error decoding chunk:[/red] {e}")

            print("\n")

            # Save assistant's response
            post_chat_message("assistant", result, username="admin")

        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted. Bye![/bold red]")
            break


if __name__ == "__main__":
    chat_with_ollama()
