import os
import platform
from distro import name as distro_name

from default_prompts import *


class PromptBuilder:
    def __init__(self) -> None:
        shell = os.path.basename(os.environ.get("SHELL", "Unknown"))
        self.os = self.__os_name()
        self.shell = os.path.basename(os.getenv("SHELL", "Unknown"))

    def shell_prompt(self, inp: str) -> str:
        inp = inp.strip()
        if not inp.endswith("?"):
            inp += "?"
        return SHELL_PROMPT.format(shell=self.shell, os=self.os, inp=inp)

    def code_prompt(self, inp: str) -> str:
        inp = inp.strip()
        if not inp.endswith("?"):
            inp += "?"
        return CODE_PROMPT.format(inp=inp)

    def do_prompt(self, inp: str, actions=[]) -> str:
        inp = inp.strip()
        if not inp.endswith("?"):
            inp += "?"
        return DO_PROMPT.format(inp=inp, actions=actions)

    def set_env_var_get_var_name_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return SET_ENV_VAR_GET_VAR_NAME_PROMPT.format(inp=inp)

    def set_env_var_get_content_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return SET_ENV_VAR_GET_CONTENT_PROMPT.format(inp=inp)

    def delete_env_var_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return DELETE_ENV_VAR_PROMPT.format(inp=inp)

    def show_env_vars_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return SHOW_ENV_VARS_PROMPT.format(inp=inp)

    def load_file_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return LOAD_FILE_PROMPT.format(inp=inp)

    def save_file_prompt(self, inp: str) -> str:
        inp = inp.strip()
        return SAVE_FILE_PROMPT.format(inp=inp)

    def __os_name(self) -> str:
        operation_system = {
            "Linux": "Linux/" + distro_name(pretty=True),
            "Windows": "Widnows " + platform.release(),
            "Darwin": "MacOS " + platform.mac_ver()[0],
        }
        return operation_system.get(platform.system(), "Unknown")
