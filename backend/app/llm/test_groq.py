from app.llm.groq_service import GroqLLMService


def main():
    llm = GroqLLMService()

    response = llm.generate(
        prompt="Explain what RAG is in one short sentence."
    )

    print("\nGroq response:")
    print(response)


if __name__ == "__main__":
    main()
