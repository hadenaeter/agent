import os
from google import genai
from google.genai import types

# list contents of a directory
def get_files_info(working_directory, directory="."):
    if directory == ".":
        return_str = "Result for current directory:"
    else:
        return_str = f"Result for '{directory}' directory:"

    # Normalize and resolve both paths
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # Check if the full_path is inside working_directory
    if not os.path.commonpath([working_directory, full_path]) == working_directory:
        return_str += f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return return_str

    # Check if final path is a directory or not
    if not os.path.isdir(full_path):
        return_str += f'\n    Error: "{directory}" is not a directory'
        return return_str

    dir_contents = os.listdir(full_path)
    contents_str_list = []

    try:
        for item_name in dir_contents:
            item_path = os.path.join(full_path, item_name)
            item_str = f"- {item_name}:"

            file_size = os.path.getsize(item_path)
            item_str += f" file_size={file_size} bytes"

            is_dir = os.path.isdir(item_path)
            item_str+= f", is_dir={is_dir}"

            contents_str_list.append(item_str)
    except Exception as e:
        return_str += f"\n    Error: {e}"
        return return_str


    for item in contents_str_list:
        return_str += f"\n{item}"

    return return_str

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
