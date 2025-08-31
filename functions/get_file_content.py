import os
from google import genai
from google.genai import types

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"\n'
    
    try:
        with open(target_file, "r") as f:

            file_content_string = f.read()

            if len(file_content_string) > MAX_CHARS:

                truncated_file_content_string = file_content_string[:MAX_CHARS+1] + f"[...File '{file_path}' truncated at 10000 characters]"

                return truncated_file_content_string
            
            return file_content_string
        
    except Exception as e:
        return f'Error: {e}\n'

#details about our get_file_content fn
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="return's the content of the file by check if given file_path exits and is file.It takes 2 args i.e. 'working_directory' and 'file_path'and this function signature is: get_file_content(working_directory, file_path). If content of the file is more than 10000 it return content upto that and also surfix it with [...File file_path truncated at 10000 characters]. It's constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get content from that file, relative to the working directory. If not provided, say so.",
            ),
        },
    ),
)