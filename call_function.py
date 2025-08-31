from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_argv = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_argv})")
    else: 
        print(f" - Calling function: {function_name}")

    working_directory = "./calculator" #we should allow ai to choice cwd thus

    match function_name:
        case "get_files_info":
            function_result = get_files_info(working_directory, **function_argv)
        case "get_file_content":
            function_result = get_file_content(working_directory, **function_argv)
        case "run_python_file":
            function_result = run_python_file(working_directory, **function_argv)
        case "write_file":
            function_result = write_file(working_directory, **function_argv)
        
        case _: #invalid fn name
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )
        
    return types.Content( 
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
        