import os
import re
import json
import logging

from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def prompt_model(model: str,
                prompt: str,
                role: str="user"):
    """Prompt the LLM model with the given prompt

    Args:
        model (str): LLM model. Either 'gpt' or 'mistral'.
        prompt (str): Prompt to be used.
        role (str, optional): user role used in prompting. Defaults to "user".

    Returns:
        message (str): Response from the model
    """
    if 'gpt' in model:
        msg = prompt_openai_model(model=model,
                        prompt=prompt,
                        role=role)
    # elif 'mistral' in model:
    #     msg = prompt_mistral_model(model=model,
    #                      role=role,
    #                      prompt=prompt)
    elif model.startswith("deepseek/") or model.startswith("openai/") or model.startswith("microsoft/") or model.startswith("mistral/"):
        msg = prompt_openrouter_model(model=model,
                                      prompt=prompt,
                                      role=role)
        logging.info(f"→ Routing to OpenRouter for model={model!r}")
    else:
        logging.info(f"Model not recognized: {model}")
        msg = None

    return msg


def prompt_openai_model(model: str,
                        prompt: str,
                        role: str="user"):
    """Prompt the OpenAI model with the given prompt

    Args:
        model (str): OpenAI model. Either 'gpt' 
        prompt (str): Prompt to be used.
        role (str, optional): user role used in prompting. Defaults to "user".

    Returns:
        message (str): Response from the model
    """
    # add in .zschrc file "export MISTRAL_API_KEY='%yourkey'"
    # run in terminal: source ~/.zshrc	
    try:
        api_key = os.environ["OPENAI_API_KEY"]
    except KeyError:
        logging.info("OPENAI_API_KEY not found")
        return None
    # connect to openai API via client
    client = OpenAI(api_key=api_key)

    # prompt the model
    res = client.chat.completions.create(
        messages=[{"role": role,
                   "content": prompt,
                   }],
        model=model,
    )
    
    # extract message from response
    msg = res.choices[0].message.content
    return msg


def prompt_mistral_model(model: str,
                         role: str,
                         prompt: str):
    """Prompt the MISTRAL model with the given prompt

    Args:
        model (str): mistral model
        role (str): user role used in prompting. Defaults to "user".
        prompt (str): Prompt to be used.

    Returns:
        message (str): Response from the model
    """
    # add in .zschrc file "export MISTRAL_API_KEY='%yourkey'"
    try:
        api_key = os.environ["MISTRAL_API_KEY"]
    except KeyError:
        logging.info("MISTRAL_API_KEY not found")
        return None
    # connect to mistral  API via client
    client = MistralClient(api_key=api_key)
    
    # prompt the model
    res = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=[ChatMessage(role=role,
                              content=prompt)],
    )
    
    # extract message from response
    msg = res.choices[0].message.content
    return msg


def prompt_openrouter_model(model: str,
                            prompt: str,
                            role: str = "user",
                            max_retries: int = 3):
    """Prompt a model hosted on OpenRouter via the OpenAI SDK compatibility layer."""
    
    try:
        api_key = os.environ["OPENROUTER_API_KEY"]
    except KeyError:
        logging.info("OPENROUTER_API_KEY not found")
        return None

    # point OpenAI client at OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for attempt in range(1, max_retries +1):
        try:
            res = client.chat.completions.create(
                # route through OpenRouter; pass through any model name they support
                model=model,  
                messages=[{"role": role, "content": prompt}],
            )
        except Exception as e:
            logging.warning(f"OpenRouter call failed (attempt {attempt}/{max_retries}): {e}")
            res = None

        if res and getattr(res, 'choices', None):
            msg = res.choices[0].message.content
            if msg is not None:
                logging.info(f"OpenRouter call: model={model!r}, prompt={prompt[:30]!r}…")
                return msg
            
        if attempt < max_retries:
            logging.info(f"Retry {attempt} failed")

    logging.error(f"OpenRouter failed after {max_retries} attempts.")
    return None


# def extract_json_as_dict(json_file: str) -> dict:
#     """Extract JSON file as dictionary

#     Args:
#         json_file (str): JSON file

#     Returns:
#         dict: dictionary
#     """
#     try:
#         dictionary = json.loads(json_file)
#         return dictionary
#     except(ValueError, json.JSONDecodeError):
#         logging.info("JSON decode error")
#         logging.info(json_file)
#         return None


# commented out function from upstream as it does not work for deepseek; use this instead
def extract_json_as_dict(json_file: str) -> dict:
    """
    Extract JSON file as dictionary.
    Strips any Markdown ```json …``` fences before parsing.
    """
    # 1) Remove any leading ```json and trailing ```
    clean_json = re.sub(r"```json\s*|\s*```", "", json_file, flags=re.IGNORECASE)
    try:
        return json.loads(clean_json)
    except (ValueError, json.JSONDecodeError):
        logging.info("JSON decode error after stripping fences:")
        logging.info(clean_json)
        return None
