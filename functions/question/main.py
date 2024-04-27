import json
from dataclasses import dataclass
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



def lambda_handler(event, context):
    
    body = json.loads(event["body"])
    
    question = body["question"]
    
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(openai_api_key="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")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(question, k=10)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)

    model = ChatOpenAI(openai_api_key="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")
    response_text = model.invoke(prompt)


    return {
        "statusCode": 200,
        "body": json.dumps({"answer": response_text.content})
    }
