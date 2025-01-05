from langchain_community.callbacks import get_openai_callback
from config import get_config


config = get_config()


def search_documents(query: str, username: str):
    results = config.search.search(
        query,
        filter=f"username eq '{username}'"
    )
    documents = []
    for result in results:
        documents.append(result["content"])
    return documents if documents else None


def generate_response(query, documents, username):
    document_string = "\n".join(documents)
    prompt = f"""
    With the following context and documents provided:
    {document_string}
    answer the query:
    {query}
    """

    # Initialize communication with the Azure OpenAI model
    try:
        # Format prompt for the model
        with get_openai_callback() as cb:
            output = config.llm.invoke(prompt)
            ret = output.content.strip()
    except Exception as e:
        raise Exception(f"Error during prompt classification: {str(e)}")

    return ret


def process_query(query: str, username: str):
    """
    Process the user query by searching for relevant documents and generating a response.

    :param query: The user query.
    :param username: The username of the user.
    :return: The response generated based on the query and documents.
    """
    documents = search_documents(query, username)
    if documents:
        response = generate_response(query, documents, username)
        return {"response": response}
    else:
        return {"response": "Sorry, there are no relevant documents found for the query."}
