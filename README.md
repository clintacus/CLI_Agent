# Command Line Interface AI Agent

## Description

This will allow you to prompt Google Gemini to read , edit, and create files within a set directory on your machine.

It will also be able to execute python scripts. 

## Set up

1. Pull the files down from locally
2. Create a .env file inside the CLI_Agent folder. 
3. Inside of the .env file enter GEMINI_API_KEY="(your API key here)" (API key can be generated from https://aistudio.google.com/api-keys)

## Configurations

Configurations can be made in the config.py file.

<u>MAX_CHARACTERS:</u> The maximum number of characters the LLM will read from a file. This is to set to prevent large amount of token usage if a large file is read.

<u>SYSTEM_PROMPT:</u> The setup prompt fed to the LLM before follow up messages are sent via the command line.

<u>WORKING_DIR:</u> The directory the LLM will have access to work in. It can access this directory and any other directories within it, but can not access higher level directories.

<u>MAX_ITERS:</u> The maximum number of iterations the LLM can perform in one session. This limits overall API usage and prevents potential infinite iterations.

<u>MODEL:</u> The Gemini model name to be used.

## How to use

From the command line while in the CLI_Agent folder run uv run main.py "(Prompt to the LLM)" [--verbose]

Optional verbose tag includes your prompt and token usage in the output.
