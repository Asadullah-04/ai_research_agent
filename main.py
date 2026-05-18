import sys
from config import ANTHROPIC_API_KEY
from agent import run_agent


def check_api_key():
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)


def main():
    check_api_key()

    print("=" * 50)
    print("  AI Research Agent")
    print("  Type 'exit' or press Ctrl+C to quit")
    print("=" * 50)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye.")
            break

        print()
        answer = run_agent(user_input)
        print(f"\nAgent: {answer}")
        print()
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()
