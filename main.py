import argparse

from prompt_builder import PromptBuilder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--script_path", help="Path to the script to run", required=False)
    parser.add_argument("--script_args", nargs=argparse.REMAINDER,
                        help="Arguments to pass to the script")
    parser.add_argument("--cautious", action="store_true")
    args = parser.parse_args()
    script_path = args.script_path
    script_args = args.script_args
    cautious = args.cautious

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


if __name__ == "__main__":
    main()
