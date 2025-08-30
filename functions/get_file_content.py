import os
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
