# GPT-SHell

This is an on-going development of an upgraded version of the original [Shell GPT](https://github.com/TheR1D/shell_gpt).
In addition to executing basic shell commands as Shell GPT already supports, with GPT-SHell, you can directly load the content of text files from your device and process them with ChatGPT.

## Introduction by GPT3.5

https://user-images.githubusercontent.com/7350056/227848106-d8d3d6d4-9f3e-4f40-82b4-5a7ee1f69988.mov

The code defines a Python script that runs a shell-like command interface using OpenAI's GPT (Generative Pretrained Transformer) language model. It imports several modules such as argparse, json, os, readline, typer, and custom-made modules such as openai_client, prompt_builder, shell_actions, think_actions, and utils.

The script initializes variables to store and manage the command history for the user, and it sets up an event handler to respond to certain keyboard events such as arrow keys and the Ctrl-C (SIGINT) signal.

The main function of the code defines an argument parser to handle command-line arguments specified when running the script. The script can be run with options such as a path to a script to run, cautious mode, or temperature. If a script path is provided, it raises a NotImplementedError since script execution is not implemented yet.

Otherwise, the script enters an infinite loop, prompting the user to input a command. It then checks if the command is one of the specific commands that trigger different actions, such as SHELL, DO, THINK, or CODE. For SHELL commands, it sends the prompt to the GPT language model and responds with the model's generated text (which may include a command to execute). If the response is a valid command, it prompts the user to confirm whether or not to run that command. For DO and THINK, the script executes shell or Python code specified in the command. For CODE, it sends the prompt to the GPT model to generate code to return.

The script also includes options for cautious mode, which displays the prompt before executing the command, and for temperature, which regulates the creativity of the GPT response. Finally, when the user inputs "exit", the script saves environment variables to a JSON file and writes the command history to a file before terminating the program.

## Install

`pip install gpt-sh`
When you first uses `gpt-sh`, you will be prompt to enter your OpenAI API key.
You can also set the following variable in `~/.config/shell_gpt/.sgptrc`.

```
OPENAI_API_KEY=[YourAPIKey]
```

## Dependency

```
shell_gpt
```

## Usage

First type in the terminal `gpt-sh`. This will start up the prompt.

Unlike the original Shell GPT, GPT-SHell functions like an actual shell, where you enter a command and then get a response.
There are four types of commands: `DO`, and `THINK`, `SHELL`, `CODE`.

### DO

This is a NEW command of GPT-SHell.
This is used to interact with GPT-SHell itself.
You can use DO command to read or write files from your device, access environment variables, etc.

There are two DO commands implemented: `SHOW_ENV_VARS`, `LOAD_FILE`.
More will be implemented in the near future.
You do not need to know the exact name of these commands. Based on your input, GPT-SHell will automatically detect the action you want to take. If it cannot determine the action, it will show you a list of all actions.

#### SHOW_ENV_VARS

This action let you check all the environment variables of GPT-SHell.
This is NOT for checking the environment variables of your OS.

When there is no environment variable, the following is shown.

```
>>> DO: Show me all the env vars
No environment variables loaded.
```

When there are environment variables, the following is shown.

```
>>> DO: Show all env vars
FILE_CONTENT_VAR_1 = Created a dynamic, customizable dashboard supporti...
FILE_CONTENT_VAR_2 = JavaScript,TypeScript,HTML5,CSS3,Python, ReactJS, ...
```

```
>>> DO: Show var: FILE_CONTENT_VAR_1
FILE_CONTENT_VAR_1 = Created a dynamic, customizable dashboard supporti...
```

Currently, the first 50 characters of each value is printed. In the future, a feature that let user to specify the print length will be implemented.

#### SET_ENV_VAR

This action let you save values to a variable.
The value can be a raw value, such as a number or a string.
The value can be the one stored in another variable.
The value can be the latest response from CODE or THINK commands.

```
>>> DO: Set the value of KEYS_CONTENT to FILE_CONTENT_VAR_2 SET_ENV_VAR
Setting the variable with name KEYS_CONTENT
>>> DO: Set the value of DESC_CONTENT to FILE_CONTENT_VAR_1 SET_ENV_VAR
Setting the variable with name DESC_CONTENT
>>> DO: Show all env vars
DESC_CONTENT = Created a dynamic, customizable dashboard supporti...
KEYS_CONTENT = JavaScript, TypeScript, HTML5, CSS3, Python, React...

>>> DO: Set the value of LETTERS to be "ABC"
Setting the variable with name LETTERS
>>> DO: show var: LETTERS
 LETTERS = ABC
```

#### DELETE_ENV_VAR

This action let you delete a variable that is no longer needed.

```
>>> DO: delete the vars: FILE_CONTENT_VAR_1, FILE_CONTENT_VAR_2
Variable FILE_CONTENT_VAR_1 deleted.
Variable FILE_CONTENT_VAR_2 deleted.
>>> DO: show vars
DESC_CONTENT = Created a dynamic, customizable dashboard supporti...
KEYS_CONTENT = JavaScript, TypeScript, HTML5, CSS3, Python, React...
ANALYSIS = SENT: Created a dynamic, customizable dashboard su...
LETTERS = ABC
```

#### LOAD_FILE

This action let you load the content of a file into GPT-SHell.
This is one major difference or upgrade from the original Shell GPT.
You can specify the paths of the files you want to load.

```
>>> DO: Load the following files. "/Users/timowang/Documents/test-sgpt/desc.txt" and "/Users/timowang/Documents/test-sgpt/keys.txt"
>>> DO: Show all env vars
FILE_CONTENT_VAR_1 = Created a dynamic, customizable dashboard supporti...
FILE_CONTENT_VAR_2 = JavaScript,TypeScript,HTML5,CSS3,Python, ReactJS, ...
```

#### SAVE_FILE

This action let you save the value of a variable to your local file system.

```
>>> DO: save the value of ANALYSIS to /tmp/analysis.txt
Saving ANALYSIS to /tmp/analysis.txt.
>>> SHELL: show the content of /tmp/analysis.txt and only show the first 5 lines
COMMAND: head -n 5 /tmp/analysis.txt
Run this command? [y/N]: y
SENT: Created a dynamic, customizable dashboard supporting various widgets to display the issue count for each template, the trend of issue count throughout a certain number of days, etc. using Material-UI components for React.
KEYS: ReactJS, Material-UI

SENT: Refactored common properties of widgets such as widget titles, subtitles, and configuration menu wrapper to a shared component, enabling cleaner implementation and easier creation of new widgets.
KEYS:
```

### THINK

This command is for you to build ChatGPT prompt using the content of the files you loaded and stored in the environment variables.
For example, in the above snippet, we loaded the description of a front-end project as well as keywords related to front-end job skills into two variables: `FILE_CONTENT_VAR_1` and `FILE_CONTENT_VAR_2`. We can now use them to build a new prompt to get sentences from the description that contain certain keywords.

```
>>> THINK: Given the following keywords: FILE_CONTENT_VAR_2.\n Given the following text: FILE_CONTENT_VAR_1. Identify all sentences that contain the keywords. Print with the following format: SENT: [A sentence with keywords]\nKEYS: [All keywords that occur in the sentence].

Your THINK prompt is:  Given the following keywords: JavaScript,TypeScript,HTML5,CSS3,Python, ReactJS, jQuery, Bootstrap, Material-UI, RESTful API, ExpressJS, NodeJS, Microservices, Figma, Docker, Git, MongoDB, PostgreSQL, MySQL, Amazon Web Service(AWS), Google Cloud Platform(GCP), Vercel.\n Given the following text: Created a dynamic, customizable dashboard supporting various widgets to display the issue count for each template, the trend of issue count throughout a certain number of days, etc. using Material-UI components for React. Refactored common properties of widgets such as widget titles, subtitles, and configuration menu wrapper to a shared component, enabling cleaner implementation and easier creation of new widgets.

Built an interface allowing admin users to configure issue templates with customizable input options such as name, type and more. Implemented dynamically rendered issue submission forms based on the conditional rendering of different input options into MUI input components by specified input options.

Created an interface for issue owners of a particular category of issues to view the details of an issue, respond to the issue, and mark keywords that serve as evidence for particular attributes of the issue, enabling future training of machine learning models for automatic attribute classification.

Implemented ExpressJS backend endpoints for retrieving template data and issue-related statistics such as issue counts and attributes. Connected the backend to MongoDB Atlas via Mongoose for better scalability and data management. Leveraged Faker.js to generate mock data for testing the implementation of the application, ensuring robustness and reliability. Containrized the backend with Docker and deployed to Google Cloud Platform.

Developed a basic authentication mechanism, storing user info in localStorage upon successful login and clears it upon logout. Implemented the frontend routing using React Router and ensured unauthorized users are redirected to an error page. . Identify all sentences that contain the keywords. Print with the following format: SENT: [A sentence with keywords]\nKEYS: [All keywords that occur in the sentence].
SENT: Created a dynamic, customizable dashboard supporting various widgets to display the issue count for each template, the trend of issue count throughout a certain number of days, etc. using Material-UI components for React.
KEYS: ReactJS, Material-UI

SENT: Refactored common properties of widgets such as widget titles, subtitles, and configuration menu wrapper to a shared component, enabling cleaner implementation and easier creation of new widgets.
KEYS: JavaScript

SENT: Built an interface allowing admin users to configure issue templates with customizable input options such as name, type and more.
KEYS: None

SENT: Implemented dynamically rendered issue submission forms based on the conditional rendering of different input options into MUI input components by specified input options.
KEYS: Material-UI

SENT: Created an interface for issue owners of a particular category of issues to view the details of an issue, respond to the issue, and mark keywords that serve as evidence for particular attributes of the issue, enabling future training of machine learning models for automatic attribute classification.
KEYS: None

SENT: Implemented ExpressJS backend endpoints for retrieving template data and issue-related statistics such as issue counts and attributes.
KEYS: ExpressJS

SENT: Connected the backend to MongoDB Atlas via Mongoose for better scalability and data management.
KEYS: MongoDB

SENT: Leveraged Faker.js to generate mock data for testing the implementation of the application, ensuring robustness and reliability.
KEYS: None

SENT: Containrized the backend with Docker and deployed to Google Cloud Platform.
KEYS: Docker, Google Cloud Platform

SENT: Developed a basic authentication mechanism, storing user info in localStorage upon successful login and clears it upon logout.
KEYS: JavaScript

SENT: Implemented the frontend routing using React Router and ensured unauthorized users are redirected to an error page.
KEYS: ReactJS
```

### SHELL

This is the same as the shell command supported by Shell GPT.
You can describe some action you want to perform with the shell, GPT-SHell will translate your command into a shell script and then execute your command.

```
>>> SHELL: Create five files with names from one to five and type of txt in /tmp
COMMAND: touch /tmp/{1..5}.txt
Run this command? [y/N]: y
```

### CODE

This is the same as the code command supported by Shell GPT.
You can describe the functionality of some code and have GPT write it for you.

```
>>> CODE: Write a c function for summing up an array.
int sumArray(int arr[], int len) {
   int sum = 0;
   for (int i = 0; i < len; i++) {
      sum += arr[i];
   }
   return sum;
}
```

## Full Example

In the `example` directory, you can find three `.txt` files.
The file `desc.txt` contains the description of a frontend project and
`keys.txt` contains skill keywords related to frontend job market.
We want to identify sentences in `desc.txt` with keywords that are listed in `keys.txt`.
Following the commands in `example_inputs.txt`, shown below as well, we can first load the files,
build a prompt with the content of the files, get analysis report, and save the report to a local file.

```
DO: Load the following files. "/Users/timowang/Developer/shell_gpt2/example/desc.txt" and "/Users/timowang/Developer/shell_gpt2/example/keys.txt"
DO: Show all env vars
DO: Set the value of DESC_CONTENT to FILE_CONTENT_VAR_1
DO: Set the value of KEYS_CONTENT to FILE_CONTENT_VAR_2
DO: delete the following variables: FILE_CONTENT_VAR_1, FILE_CONTENT_VAR_2
THINK: Given the following keywords: KEYS_CONTENT.\n Given the following text: DESC_CONTENT. Identify all sentences that contain the keywords. Print with the following format: SENT: [A sentence with keywords]\nKEYS: [All keywords that occur in the sentence].
DO: Save the LAST_RESPONSE to a variable called "ANALYSIS"
DO: Show all env vars
DO: Save the value of ANALYSIS to the file /tmp/analysis.txt
SHELL: Print out the first 3 lines of the content of /tmp/analysis.txt
```

You can also execute pre-defined scripts line by line automatically as follows.

```
gpt-sh --script_path example/example_inputs.txt
```

## Limitations

Currently GPT-SHell is still under active development.
Unlike Shell GPT, which focuses on serving as a command-line interface for accessing GPT functionalities, such as a chat,
GPT-SHell focuses on helping you processing files on your own device.
No matter the task is summarizing the content of a long report, or creating new content and then saving it on your device for you directly, GPT-SHell (at least the future version) will be your best helper!

## Upcoming features

These are the features being developed right now. You can also suggest features in the Discussion/Issues section.

### General Interactions

- Support basic shell commands without making requests to OpenAI apis such as ls, cd, etc.

### DO Commands

## Acknowledgement

This project is an extended version based on [shell_gpt](https://github.com/TheR1D/shell_gpt) by TheR1D.
