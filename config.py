# Maximum number of characters to read from a file
MAX_CHARACTERS = 10000

# System prompt for the AI agent
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Set your desired working directory here
WORKING_DIR = "./calculator"

# Set the maximum number of iterations the agent can perform in a single session
MAX_ITERS = 20

# Specify the model to use
MODEL = "gemini-2.0-flash-001"