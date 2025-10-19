import os

def write_file(working_directory, file_path, content):

    # Ensure the file path is within the working directory
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if file path leads to a valid file if not create it
    dir_name = os.path.dirname(target_path)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception as e:
            return f'Error: Cannot create directory "{dir_name}": {e}'
    
    # Write content to the file
    try:
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file: {e}"