import os

def write_file(working_directory, file_path, content):
    return_str = f"Result for '{file_path}' file:"
    # Normalize and resolve both paths
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the full_path is inside working_directory
    if not os.path.commonpath([working_directory, full_path]) == working_directory:
        return_str += f'\n    Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        return return_str

    # Check if full_path exists, if it does, check if it is a file
    if os.path.exists(full_path):
        if not os.path.isfile(full_path):
            return_str += f'\n    Error: File not found or is not a regular file: "{file_path}"'
            return return_str
    else:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open (full_path, "w") as f:
            f.write(content)

        return_str += f'\nSuccessfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return_str += f"\n    Error: {e}"
        return return_str

    return return_str
