from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():

    query_text = input("Make a question about Lambda Forge: ")

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key="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")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=10)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(openai_api_key="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")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text.content}\nSources: {list(set(sources))}"
    formatted_response = f"\033[93m\nResponse: {response_text.content}\n\033[0m"
    print(formatted_response)


if __name__ == "__main__":
    main()