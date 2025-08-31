import os
import subprocess
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args) #extend not append cuz args is list and we want to add each...
        result = subprocess.run(
            commands,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

#details about our run_python_file fn
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""runs the python file by taking working_directory, file_path and agrs. function signature is run_python_file(working_directory, file_path, args=None). it uses subprocess.run from subprocess module. the given cmd in subprocess.run is commands = ["python", abs_file_path]
        if args:
            commands.extend(args) #extend not append cuz args is list and we want to add each...
        result = subprocess.run(
            commands,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        ), constrained to the working directory.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to run it, relative to the working directory. If not provided, say so.",
            ),
        },
    ),
)