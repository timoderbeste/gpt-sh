import argparse
import json
import os
import typer

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder
from shell_actions import handle_shell_action
from think_actions import handle_think_action
from utils import (
    typer_writer,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--script_path", help="Path to the script to run", required=False)
    parser.add_argument("--script_args", nargs=argparse.REMAINDER,
                        help="Arguments to pass to the script")
    parser.add_argument("--cautious", action="store_true")
    parser.add_argument("--temperature", type=float, default=1)
    args = parser.parse_args()
    script_path = args.script_path
    script_args = args.script_args
    cautious = args.cautious
    temperature = args.temperature

    prompt_builder = PromptBuilder()

    try:
        with open(os.path.join(os.getenv("HOME"), ".config", "shell_gpt", "env_var2val.json"), "r") as fp:
            env_var2val = json.load(fp)
    except FileNotFoundError:
        env_var2val = dict()

    if script_path:
        raise NotImplementedError("Script path is not implemented yet")
    else:
        while True:
            inp = input(">>> ")
            if inp == "exit":
                with open(os.path.join(os.getenv("HOME"),
                                       ".config", "shell_gpt",
                                       "env_var2val.json"), "w") as fp:
                    json.dump(env_var2val, fp)
                break

            if inp.startswith("SHELL: "):
                inp = inp.replace("SHELL: ", "")
                prompt = prompt_builder.shell_prompt(inp)
                response = get_gpt_response(
                    prompt, temperature=temperature, top_p=1, caching=False, chat=None)
                typer_writer(response, code=True,
                             shell=True, animate=True)
                if response.startswith("COMMAND: "):
                    response = response.replace("COMMAND: ", "")
                    if typer.confirm("Run this command?"):
                        os.system(response)
                else:
                    print(response)
                    print(
                        "The response is not a command. This is a bug from OpenAI.")
            elif inp.startswith("DO: "):
                successful = handle_shell_action(inp, env_var2val, temperature)
                if not successful:
                    print("Action failed. Please try again.")
            elif inp.startswith("THINK: "):
                handle_think_action(inp, env_var2val, temperature)
            elif inp.startswith("CODE: "):
                inp = inp.replace("CODE: ", "")
                prompt = prompt_builder.code_prompt(inp)
                response = get_gpt_response(
                    prompt, temperature=temperature, top_p=1, caching=False, chat=None)
                typer_writer(response, code=True,
                             shell=False, animate=True)
            if cautious:
                print(prompt)


if __name__ == "__main__":
    main()
