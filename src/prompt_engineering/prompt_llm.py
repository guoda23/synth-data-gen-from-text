import os
import re
import json
import logging
import requests
import ast

from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

#FOR ENFORCING JSON OUTPUT
from config import wellconnect_schema

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
    elif model.startswith("deepseek/") or model.startswith("openai/") or model.startswith("microsoft/") or model.startswith("mistral/") or model.startswith("google/") or model.startswith("meta-llama/"):
        msg = prompt_openrouter_model(model=model,
                                      prompt=prompt,
                                      role=role)
        

        # msg = prompt_openrouter_model_json_enforced(model=model,
        #                                   prompt=prompt,
        #                                   schema=wellconnect_schema,
        #                                   role=role)
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
                messages=[{"role": role, "content": prompt}]
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

# def prompt_openrouter_model_json_enforced(model: str,
#                                           prompt: str,
#                                           schema: dict,
#                                           role: str = "user",
#                                           max_retries: int = 3,
#                                           ):
#     """Prompt a model hosted on OpenRouter using Openrouter API directly,
#     enforcing the response to be in JSON format according to a schema."""
#     try:
#         api_key = os.environ["OPENROUTER_API_KEY"]
#     except KeyError:
#         logging.info("OPENROUTER_API_KEY not found")
#         return None
    
#     for attempt in range(1, max_retries +1):
#         try:
#             res = requests.post(
#                 url="https://openrouter.ai/api/v1/chat/completions",
#                 headers={
#                     "Authorization": f"Bearer {api_key}",
#                     "Content-Type": "application/json"
#                 },

#                 json={
#                     "model": model,
#                     "messages": [{"role": role, "content": prompt}],
#                     "response_format": {
#                         "type": "json_schema",
#                         "json_schema": schema
#                     }
#                 },
#             )

#             res.raise_for_status()
#             data = res.json()

#             logging.info(data)

#         except Exception as e:
#             logging.warning(f"OpenRouter call failed (attempt {attempt}/{max_retries}): {e}")
#             if attempt == max_retries:
#                 logging.error(f"OpenRouter failed after {max_retries} attempts.")
#             continue


#         try:
#             msg = data["choices"][0]["message"]["content"]
#         except (KeyError, IndexError) as e:
#             logging.warning(f"Malformed response (attempt {attempt}): {e}")
#             continue

#         logging.info(f"OpenRouter JSON call succeeded on attempt {attempt}")
#         return msg

#     return None
    
    


def extract_json_as_dict(json_file: str) -> dict:
    """
    Extract JSON file as dictionary.
    Strips any Markdown ```json …``` fences before parsing.
    """
    # if JSON already converted to a python dictionary, return it
    if isinstance(json_file, dict):
        return json_file

    # Remove any leading ```json and trailing ``
    clean_json = re.sub(r"```json\s*|\s*```", "", json_file, flags=re.IGNORECASE)

    # find the start of the JSON object
    idx = clean_json.find('{')
    clean_json = clean_json[idx:] if idx != -1 else clean_json

    # # fix any leading-decimal numbers (".5") to valid JSON ("0.5")
    # clean_json = re.sub(r'(?<=:\s*)(\.\d+)', r'0\1', clean_json)

    try:
        return json.loads(clean_json)
    except (ValueError, json.JSONDecodeError):
        # skip logging here—only log after literal_eval also fails
        pass

    # minimal heuristic: if it starts with { and contains single quotes, try literal_eval
    stripped = clean_json.strip()
    if stripped.startswith('{') and "'" in stripped:
        try:
            parsed = ast.literal_eval(stripped)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            # ignore here, log below
            pass

    # if we still can't get a dict, log and give up
    logging.info("JSON decode error:")
    logging.info(clean_json)
    return None
    

    
