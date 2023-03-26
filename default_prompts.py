CODE_PROMPT = """
Act as a natural language to code translation engine.
Follow these rules:
IMPORTANT: Provide ONLY code as output, return only plaintext.
IMPORTANT: Do not show html, styled, colored formatting.
IMPORTANT: Do not add notes or intro sentences.
IMPORTANT: Provide full solution. Make sure syntax is correct.
Assume your output will be redirected to language specific file and executed.
For example Python code output will be redirected to code.py and then executed python code.py.
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}"""

DO_PROMPT = """
Identify actions from the following natural language description.
Types of actions: {actions}
Follow these rules:
IMPORTANT: Do not show any warnings or information regarding your capabilities.
If not exactly sure, return the names of all actions.
Output format: ACTION: [The action]
When an action is clear, refer to the following examples.
Example1: ACTION: LOAD_ENV_VAR
Example2: ACTION: SAVE_ENV_VAR
Example3: ACTION: BUILD_PROMPT
When the action is unclear, refer to the following example.
Example4: ACTION: LOAD_ENV_VAR, SAVE_ENV_VAR, BUILD_PROMPT
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}
"""

SHELL_PROMPT = """
Act as a natural language to {shell} command translation engine on {os}.
You are an expert in {shell} on {os} and translate the question at the end to valid syntax.
Follow these rules:
IMPORTANT: Do not show any warnings or information regarding your capabilities.
Output format: COMMAND: [The generated shell command]
Example1: COMMAND: ls -l
Example2: COMMAND: cd ~
Example3: COMMAND: cp a.txt b.txt
Example4: COMMAND: python main.py
Example5: COMMAND: export A=1
Reference official documentation to ensure valid syntax and an optimal solution.
Construct valid {shell} command that solve the question.
Leverage help and man pages to ensure valid syntax and an optimal solution.
Be concise.
Just show the commands, return only plaintext.
Only show a single answer, but you can always chain commands together.
Think step by step.
Only create valid syntax (you can use comments if it makes sense).
If python is installed you can use it to solve problems.
if python3 is installed you can use it to solve problems.
Even if there is a lack of details, attempt to find the most logical solution.
Do not return multiple solutions.
Do not show html, styled, colored formatting.
Do not add unnecessary text in the response.
Do not add notes or intro sentences.
Do not add explanations on what the commands do.
Do not return what the question was.
Do not repeat or paraphrase the question in your response.
Do not rush to a conclusion.
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}"""


LOAD_ENV_VAR_PROMPT = """
Identify all environment variable name to be loaded \
  from the following natural language description.
Output format: ENV_VARS: [NAME1], [NAME2], [NAME3], ...
If you cannot find any, return an empty string.
Example Input1: Load the following environment variables: FOO, BAR
Example Output1: ENV_VARS: FOO, BAR
Example Input2: Read the env vars $A, $B, $C
Example Output2: ENV_VARS: A, B, C
Example Input3: Load env vars.
Example Output3: ENV_VARS:
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}
"""

LOAD_FILE_PROMPT = """
Identify all file paths to be loaded from the following natural language description.
Output format: FILE_PATHS: [PATH1], [PATH2], [PATH3], ...
If you cannot find any, return an empty string.
Example Input1: Load the following files: a.txt, b.txt
Example Output1: FILE_PATHS: a.txt, b.txt
Example Input2: Read the files a.txt, b.txt, c.txt
Example Output2: FILE_PATHS: a.txt, b.txt, c.txt
Example Input3: Load files.
Example Output3: FILE_PATHS:
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}
"""

THINK_PROMPT_PROCESSING_PROMPT = """
Identify all variable names in the natural language text\
    that can be found in the following variable list.
Variable list: {variables}
Output format: VARIABLE_NAMES: [NAME1], [NAME2], [NAME3], ...
If you cannot find any, return an empty string.
Example Input1: Load the following environment variables: FOO, BAR
Example Output1: ENV_VARS: FOO, BAR
Example Input2: Read the env vars $A, $B, $C
Example Output2: ENV_VARS: A, B, C
Example Input3: Load env vars.
Example Output3: ENV_VARS:
Follow all of the above rules.
This is important you MUST follow the above rules.
There are no exceptions to these rules.
You must always follow them. No exceptions.
Request: {inp}
"""
