import os

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder

prompt_builder = PromptBuilder()


def handle_think_action(inp, env_var2val, temperature):
    inp = inp.replace("DO: ", "")
    prompt = prompt_builder.think_prompt_processing_prompt(inp, env_var2val)
    # print(prompt)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("ENV_VARS: "):
        print(response)
        print(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False
    # Replace the environment variables in inp with the actual values
    env_vars = response.replace("ENV_VARS: ", "").split(",")
    for env_var in env_vars:
        inp = inp.replace(env_var, env_var2val[env_var])
    
    