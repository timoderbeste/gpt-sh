import argparse
import os

from prompt_builder import PromptBuilder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", help="Path to the script to run")
    parser.add_argument("script_args", nargs=argparse.REMAINDER,
                        help="Arguments to pass to the script")
    args = parser.parse_args()
    script_path = args.script_path
    script_args = args.script_args

    