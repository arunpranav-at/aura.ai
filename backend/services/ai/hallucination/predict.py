import os
from dotenv import load_dotenv
from azure.ai.evaluation import GroundednessEvaluator
from services.ai.context.generate import context_generator
from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback
from config import get_config

load_dotenv()

config = get_config()


def hallucination_predictor_without_contextinput(query, response):
    """
    Evaluates the groundedness of a query, context, and response pair using Azure AI evaluation tools.

    Args:
        query (str): The query string to evaluate.
        response (str): The response string to evaluate.

    Returns:
        dict: A dictionary containing the groundedness score and additional information.
        eg: {'groundedness': 5.0, 'gpt_groundedness': 5.0, 'groundedness_reason': 'The response is fully correct and complete, directly answering the query with precise information from the context. It does not include any extraneous details, making it a perfect match for the definition of groundedness at level 5.'}
    """
    # Classify the prompt to determine the type of task
    prompttype = classify_prompt(query)
    if prompttype == "open-ended creative":
        return {"groundedness": 6.0, "gpt_groundedness": 6.0, "groundedness_reason": "The response to the above prompt is expected to be a type of intentional hallucination, as it is an open-ended creative task and does not require factual accuracy."}
    elif prompttype == "greeting":
        return {"groundedness": 5.0, "gpt_groundedness": 5.0, "groundedness_reason": "The given prompt is a casual or open ended statments that are typically informal and general designed to elicit conversational responses from the model,hence it is not considered as an instance of hallucination."}

    # Generate context dynamically using context_generator
    context = context_generator(query)

    return hallucination_predictor(query, response, context)


def hallucination_predictor(query, response, context):
    """
    Evaluates the groundedness of a query, context, and response pair using Azure AI evaluation tools.

    Args:
        query (str): The query string to evaluate.
        response (str): The response string to evaluate.
        context (str): The context string to evaluate.

    Returns:
        dict: A dictionary containing the groundedness score and additional information.
        eg: {'groundedness': 5.0, 'gpt_groundedness': 5.0, 'groundedness_reason': 'The response is fully correct and complete, directly answering the query with precise information from the context. It does not include any extraneous details, making it a perfect match for the definition of groundedness at level 5.'}
    """

    # Classify the prompt to determine the type of task
    prompt_type = classify_prompt(query)
    if prompt_type == "open-ended creative":
        return {"groundedness": 6.0, "gpt_groundedness": 6.0, "groundedness_reason": "The response to the above prompt is expected to be a type of intentional hallucination, as it is an open-ended creative task and does not require factual accuracy."}
    elif prompt_type == "greeting":
        return {"groundedness": 5.0, "gpt_groundedness": 5.0, "groundedness_reason": "The response is a simple greeting or salutation, which is a common social interaction and hence it is not considered as an instance of hallucination."}

    # Model Configuration
    model_config = {
        "azure_endpoint": config.env.azure_openai_endpoint,
        "api_key": config.env.azure_openai_api_key,
        "azure_deployment": config.env.azure_openai_deployment,
        "api_version": config.env.azure_openai_api_version
    }

    # Initializing Groundedness and Groundedness Pro evaluators
    groundedness_eval = GroundednessEvaluator(model_config)

    # Define query-response pair
    query_response = dict(
        query=query,
        context=context,
        response=response
    )

    # Run the evaluator and return the score
    groundedness_score = groundedness_eval(**query_response)
    return groundedness_score


def classify_prompt(prompt: str):
    """
    Classifies the input prompt into one of the following categories:
    - "factual" (direct questions with a specific answer)
    - "fact-based creative" (creative tasks grounded in factual content)
    - "open-ended creative" (imaginative or artistic tasks with no factual context)
    - "greeting" (simple greetings or salutations)

    Args:
        prompt (str): The user input prompt to classify.

    Returns:
        str: The classification category ("factual", "fact-based creative", "open-ended creative", or "greeting").
    """

    # Fixed classification prompt template
    classification_prompt = f"""
    Classify the following prompt into one of the categories:
    1. "factual" - Direct questions or commands with a specific and verifiable answer.
    2. "fact-based creative" - Creative prompts that involve factual topics or entities (e.g., essays, descriptions).
    3. "open-ended creative" - Purely imaginative prompts without a factual basis (e.g., poems, fictional stories).
    4. "greeting" - Simple greetings or salutations.

    Example classifications:
    - "Write a poem about love." → open-ended creative
    - "Generate a paragraph on the Taj Mahal." → fact-based creative
    - "What is the height of the Taj Mahal?" → factual
    - "Create a fantasy story." → open-ended creative
    - "Write an essay on climate change." → fact-based creative
    - "Hello, how are you?" → greeting
    - "Hi, what's up?" → greeting

    Classify this prompt:
    {prompt}
    """

    try:
        api_key = config.env.azure_openai_api_key_gpt_4o_mini
        endpoint = config.env.azure_openai_endpoint_gpt_4o_mini
        deployment = config.env.azure_openai_deployment_gpt_4o_mini
        api_version = config.env.azure_openai_api_version_gpt_4o_mini

        llm = AzureChatOpenAI(
            openai_api_key=api_key,
            azure_endpoint=endpoint,
            azure_deployment=deployment,
            api_version=api_version,
            temperature=0,
            max_tokens=50,
            timeout=None,
            max_retries=2,
        )

        with get_openai_callback() as cb:
            output = llm.invoke(classification_prompt)
            ret = output.content.strip()

    except Exception as e:
        raise Exception(f"Error during prompt classification: {str(e)}")

    return ret
