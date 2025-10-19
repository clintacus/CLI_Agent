import os
from config import MAX_CHARACTERS
from google.genai import types

# Set up schema for the function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARACTERS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    # Ensure the file path is within the working directory
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if file path leads to a valid file
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read file content up to MAX_CHARACTERS and return it
    try:
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
    
        if len(file_content_string) == MAX_CHARACTERS:
            file_content_string += '[...File "{file_path}" truncated at 10000 characters]'
        
        return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"