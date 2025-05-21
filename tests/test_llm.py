import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load .env file

    llm = ChatOpenAI(
    model_name="mistralai/mistral-medium-3",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    max_tokens=500  # limit to 500 tokens output max
)


    response = llm.invoke([HumanMessage(content="Hello! What is Retrieval-Augmented Generation?")])
    print("Response:", response.content)

if __name__ == "__main__":
    main()
