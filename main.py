import argparse

from config import config
from openai_client import OpenAIClient
from prompt_builder import PromptBuilder
from utils import (
    loading_spinner,
    echo_chat_ids,
    echo_chat_messages,
    typer_writer,
    get_edited_prompt,
)


@loading_spinner
def get_completion(
    prompt: str,
    temperature: float,
    top_p: float,
    caching: bool,
    chat: str,
):
    api_host = config.get("OPENAI_API_HOST")
    api_key = config.get("OPENAI_API_KEY")
    client = OpenAIClient(api_host, api_key)
    return client.get_completion(
        message=prompt,
        model="gpt-3.5-turbo",
        temperature=temperature,
        top_probability=top_p,
        caching=caching,
        chat_id=chat,
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
    if script_path:
        raise NotImplementedError("Script path is not implemented yet")
    else:
        while True:
            inp = input(">>> ")
            if inp == "exit":
                break
            prompt = prompt_builder.shell_prompt(inp)
            if cautious:
                print(prompt)

            generated_command = get_completion(
                prompt, temperature=temperature, top_p=1, caching=False, chat=None)
            typer_writer(generated_command, code=True,
                         shell=True, animate=True)


if __name__ == "__main__":
    main()
