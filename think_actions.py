import os

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder

prompt_builder = PromptBuilder()


def handle_think_action(inp, env_var2val, temperature):
    inp = inp.replace("THINK: ", "")
    
    for var in env_var2val:
        inp = inp.replace(var, env_var2val[var])

    prompt = inp
    print("Your THINK prompt is: ", prompt)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    print(response)
