import sys

from ai_playground.chat_session import ChatSession
from ai_playground.client import GeminiClient

client = GeminiClient()
chat_session: ChatSession = ChatSession(client)


def main() -> None:
    while True:
        try:
            prompt = input("user > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)

        if prompt == "":
            continue
        try:
            answer = chat_session.chat(prompt)
        except RuntimeError:
            continue
        print(answer)


if __name__ == "__main__":
    main()
