import os

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder
from utils import get_tmp_env_var_name

prompt_builder = PromptBuilder()
ACTIONS = ["LOAD_ENV_VAR", "SAVE_ENV_VAR",
           "BUILD_PROMPT", "LOAD_FILE", "SAVE_FILE", "SHOW_ENV_VARS"]


def handle_shell_action(inp, env_var2val, temperature) -> bool:
    inp = inp.replace("DO: ", "")
    prompt = prompt_builder.do_prompt(inp, actions=ACTIONS)
    # print(prompt)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("ACTION: "):
        print(response)
        print(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False

    response = response.replace("ACTION: ", "")
    if "," in response or response not in ACTIONS:
        print("Your input leads to multiple possible actions. Please be more specific.")
        print("Available actions: ", ACTIONS)
        return False

    action_name = response.replace("ACTION: ", "")
    print(f"Running action {action_name}")
    if action_name == "LOAD_ENV_VAR":
        return handle_load_env_var(inp, env_var2val, temperature)
    elif action_name == "LOAD_FILE":
        return handle_load_file(inp, env_var2val, temperature)
    elif action_name == "SHOW_ENV_VARS":
        return handle_show_env_vars(env_var2val)
    else:
        raise NotImplementedError("This action is not implemented yet")


def handle_load_env_var(inp, env_var2val, temperature) -> bool:
    prompt = prompt_builder.load_env_var_prompt(inp)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("ENV_VARS: "):
        print(response)
        print(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False

    response = response.replace("ENV_VARS: ", "")
    env_vars = response.split(",")
    for env_var in env_vars:
        env_var2val[env_var] = os.environ.get(env_var)
    print(env_var2val)
    return True


def handle_load_file(inp, env_var2val, temperature) -> bool:
    prompt = prompt_builder.load_file_prompt(inp)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("FILE_PATHS: "):
        print(response)
        print(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False
    response = response.replace("FILE_PATHS: ", "")
    file_paths = response.split(",")

    for file_path in file_paths:
        file_path = file_path.strip()
        new_env_var_name = get_tmp_env_var_name(env_var2val)
        try:
            with open(file_path, "r") as fp:
                env_var2val[new_env_var_name] = fp.read()
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return False
    return True


def handle_show_env_vars(env_var2val) -> bool:
    print(env_var2val)
    return True
