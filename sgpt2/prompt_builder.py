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
    
    def load_env_var_prompt(self, inp: str) -> str:
        inp = inp.strip()
        if not inp.endswith("?"):
            inp += "?"
        return LOAD_ENV_VAR_PROMPT.format(inp=inp)
    
    def load_file_prompt(self, inp: str) -> str:
        inp = inp.strip()
        if not inp.endswith("?"):
            inp += "?"
        return LOAD_FILE_PROMPT.format(inp=inp)

    def __os_name(self) -> str:
        operation_system = {
            "Linux": "Linux/" + distro_name(pretty=True),
            "Windows": "Widnows " + platform.release(),
            "Darwin": "MacOS " + platform.mac_ver()[0],
        }
        return operation_system.get(platform.system(), "Unknown")
    