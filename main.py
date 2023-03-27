import argparse
import json
import os
import readline
import signal
import typer

from openai_client import get_gpt_response
from prompt_builder import PromptBuilder
from shell_actions import handle_shell_action
from think_actions import handle_think_action
from utils import typer_writer

history_commands = []

history_file = os.path.join(os.getenv("HOME"),
                            ".config", "shell_gpt",
                            "history_commands.json")
try:
    readline.read_history_file(history_file)
except FileNotFoundError:
    pass

try:
    with open(os.path.join(os.getenv("HOME"), ".config", "shell_gpt", "env_var2val.json"), "r") as fp:
        env_var2val = json.load(fp)
except FileNotFoundError:
    env_var2val = dict()


def save_and_exit():
    global env_var2val
    with open(os.path.join(os.getenv("HOME"),
                           ".config", "shell_gpt",
                           "env_var2val.json"), "w+") as fp:
        json.dump(env_var2val, fp)
        readline.set_history_length(1000)
        readline.write_history_file(history_file)
        exit(0)


def handle_sigint(signal, frame):
    save_and_exit()


def key_handler(event):
    global history_commands
    if event == readline.SIGINT:
        # User pressed Ctrl-C, so clear the input line
        readline.set_line_buffer('')
        print('^C')
    elif event == readline.KEY_UP:
        # User pressed Up arrow, so get previous command from history
        if history_commands:
            readline.set_history_item(
                readline.get_current_history_length() - 1, history_commands.pop())
    elif event == readline.KEY_DOWN:
        # User pressed Down arrow, so get next command from history
        if readline.get_current_history_length() > len(history_commands):
            history_commands.append(readline.get_history_item(
                readline.get_current_history_length() - 1))
    elif event == readline.KEY_LEFT:
        # User pressed Left arrow, so move cursor left
        current_pos = readline.get_begidx()
        if current_pos > 0:
            readline.set_cursor_position(current_pos - 1)
    elif event == readline.KEY_RIGHT:
        # User pressed Right arrow, so move cursor right
        current_pos = readline.get_begidx()
        end_pos = readline.get_endidx()
        if current_pos < end_pos:
            readline.set_cursor_position(current_pos + 1)


def main():
    global history_commands, env_var2val

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
    latest_response = None

    if script_path:
        raise NotImplementedError("Script path is not implemented yet")
    else:
        readline.parse_and_bind('')
        readline.set_pre_input_hook(key_handler)
        signal.signal(signal.SIGINT, handle_sigint)
        while True:
            inp = input(">>> ")
            if inp == "exit":
                save_and_exit()

            try:
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
                    response = handle_shell_action(
                        inp, env_var2val, latest_response)
                    if not response:
                        print("Action failed. Please try again.")
                elif inp.startswith("THINK: "):
                    response = handle_think_action(
                        inp, env_var2val, temperature)
                    latest_response = response
                elif inp.startswith("CODE: "):
                    inp = inp.replace("CODE: ", "")
                    prompt = prompt_builder.code_prompt(inp)
                    response = get_gpt_response(
                        prompt, temperature=temperature, top_p=1, caching=False, chat=None)
                    latest_response = response
                    typer_writer(response, code=True,
                                 shell=False, animate=True)
                if cautious:
                    print(prompt)
            except Exception as e:
                print("Something went wrong. Please try again.")
                print(e)


if __name__ == "__main__":
    main()
