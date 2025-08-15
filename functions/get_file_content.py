import os
from google import genai
from google.genai import types
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    return_str = f"Result for '{file_path}' file:"
    # Normalize and resolve both paths
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the full_path is inside working_directory
    if not os.path.commonpath([working_directory, full_path]) == working_directory:
        return_str += f'\n    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return return_str

    # Check if full_path is a file or not
    if not os.path.isfile(full_path):
        return_str += f'\n    Error: File not found or is not a regular file: "{file_path}"'
        return return_str

    try:
        with open(full_path, "r") as f:
            file_content = f.read(MAX_CHARS)

        return_str += "\n" + file_content
        if len(file_content) >= MAX_CHARS:
            return_str += f'\n    [...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return_str += f"\n    Error: {e}"
        return return_str

    return return_str

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a specified file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to said file, within the working directory",
            ),
        },
    ),
)
