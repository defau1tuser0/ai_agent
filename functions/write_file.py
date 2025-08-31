import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path): #open() can be created file if not but dir can't thus
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
        
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"
    
#details about our write_file fn
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Takes the working_directory, file_path and content as argv and overwrite the given file from file_path with the provided content, constrained to the working directory. function signature: write_file(working_directory, file_path, content)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to overwrite the given file from file path or make a new file and then overwrite it with content, relative to the working directory. If not provided, say so.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which will be used to overwrite the given file path or make a new file, relative to the working directory. If not provided, say so.",
            ),
        },
    ),
)