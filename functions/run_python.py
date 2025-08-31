import os
import sys
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    cmd = [sys.executable, abs_file_path, *args]

    try:
        completed_process = subprocess.run(cmd, cwd=working_directory, capture_output=True, text=True, timeout=5)

        if completed_process is None:
            return f"No output produced."

        if completed_process.returncode != 0:
            return f'STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}\nProcess exited with code {completed_process.returncode}'
        return f'STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}\n'

                
    except Exception as e:
         return f"Error: executing Python file: {e}"
    
    