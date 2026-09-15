from ai_playground.chat_session import ChatSession
from ai_playground.client import GeminiClient

client = GeminiClient()
chat_session: ChatSession = ChatSession(client)


def main() -> None:
    while True:
        prompt = input("user > ").strip()
        if prompt == "":
            continue
        answer = chat_session.chat(prompt)
        print(answer)


if __name__ == "__main__":
    main()
