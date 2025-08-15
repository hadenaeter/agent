import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    return_str = f"Result for '{file_path}' file:"
    # Normalize and resolve both paths
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the full_path is inside working_directory
    if not os.path.commonpath([working_directory, full_path]) == working_directory:
        return_str += f'\n    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        return return_str

    # Check if full_path exists, if it does, check if it is a file
    if not os.path.exists(full_path):
        return_str += f'\n    Error: File "{file_path}" not found.'
        return return_str

    # Check if file is a python file, i.e. it ends with .py
    if not full_path[-3:] == ".py":
        return_str += f'\n    Error: "{file_path}" is not a Python file.'
        return return_str

    try:
        # Execute the file
        if args == []:
            result = subprocess.run(
                ["python3", full_path],
                timeout=30,
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                ["python3", full_path, ", ".join(arg for arg in args)],
                timeout=30,
                capture_output=True,
                text=True
            )

        return_str += f"\n    STDOUT:\n{result.stdout}"
        return_str += f"\n    STDERR:\n{result.stderr}"

        if result.returncode != 0:
            return_str += "\n    Process exited with code X"

        if result.stdout == "":
            return_str += "No output produced."
            return return_str
    except Exception as e:
        return_str += f"Error: executing Python file: {e}"
        return return_str

    return return_str

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python file with arguments if specified, within working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the python file to run"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="list of arguments to use for the python file to run"
            ),
        },
    ),
)
