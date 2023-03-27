import os
from pprint import pprint

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder
from utils import get_tmp_env_var_name, typer_writer

prompt_builder = PromptBuilder()
ACTIONS = [
    "LOAD_ENV_VAR", "SAVE_ENV_VAR", "SHOW_ENV_VARS",
    "RENAME_ENV_VAR", "DELETE_ENV_VAR", "CLEAR_ENV_VARS", "SET_ENV_VAR",
    "LOAD_FILE", "SAVE_FILE",
]


def handle_shell_action(inp, env_var2val, temperature) -> bool:
    inp = inp.replace("DO: ", "")
    prompt = prompt_builder.do_prompt(inp, actions=ACTIONS)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("ACTION: "):
        print(response)
        typer_writer(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False

    response = response.replace("ACTION: ", "")
    if "," in response or response not in ACTIONS:
        typer_writer(
            "Your input leads to multiple possible actions. Please be more specific.")
        typer_writer("Available actions: ", ACTIONS)
        return False

    action_name = response.replace("ACTION: ", "")
    if action_name == "LOAD_ENV_VAR":
        return handle_load_env_var(inp, env_var2val, temperature)
    elif action_name == "LOAD_FILE":
        return handle_load_file(inp, env_var2val, temperature)
    elif action_name == "SAVE_FILE":
        return handle_save_file(inp, env_var2val, temperature)
    elif action_name == "SHOW_ENV_VARS":
        return handle_show_env_vars(env_var2val)
    else:
        print(f"ACTION: {action_name} is not implemented yet.")
        return False


def handle_load_env_var(inp, env_var2val, temperature) -> bool:
    prompt = prompt_builder.load_env_var_prompt(inp)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("ENV_VARS: "):
        typer_writer(response)
        typer_writer(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False

    response = response.replace("ENV_VARS: ", "")
    env_vars = response.split(",")
    for env_var in env_vars:
        env_var2val[env_var] = os.environ.get(env_var)
    return True


def handle_load_file(inp, env_var2val, temperature) -> bool:
    prompt = prompt_builder.load_file_prompt(inp)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not response.startswith("FILE_PATHS: "):
        typer_writer(response)
        typer_writer(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False
    response = response.replace("FILE_PATHS: ", "")
    file_paths = response.split(",")

    for file_path in file_paths:
        file_path = file_path.strip()
        new_env_var_name = get_tmp_env_var_name(
            env_var2val, "FILE_CONTENT_VAR_")
        try:
            with open(file_path, "r") as fp:
                env_var2val[new_env_var_name] = fp.read()
        except FileNotFoundError:
            typer_writer(f"File {file_path} not found.")
            return False
        typer_writer(f"{file_path} loaded.")
    return True


def handle_save_file(inp, env_var2val, temperature) -> bool:
    prompt = prompt_builder.save_file_prompt(inp)
    response = get_gpt_response(
        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
    if not "FILE_PATH: " in response and "VAR_NAME: " in response:
        typer_writer(response)
        typer_writer(
            "The response is not a valid action. This is a bug from OpenAI.")
        return False
    file_path, var_name = response.split(",")
    file_path = file_path.replace("FILE_PATH: ", "").strip()
    var_name = var_name.replace("VAR_NAME: ", "").strip()
    typer_writer(f"Saving {var_name} to {file_path}.")
    try:
        with open(file_path, "w+") as fp:
            fp.write(env_var2val[var_name])
        return True
    except FileNotFoundError:
        typer_writer(f"Path {file_path} not found.")
        typer_writer(f"Formatted prompt: {prompt}")
        typer_writer(f"Untouched response: {response}")
        return False


def handle_show_env_vars(env_var2val) -> bool:
    if len(env_var2val) == 0:
        typer_writer("No environment variables loaded.")
        return True
    else:
        for env_var in env_var2val:
            typer_writer(f"{env_var} = {env_var2val[env_var][:50]}" +
                         "..." if len(env_var2val[env_var]) > 50 else "")
        return True
