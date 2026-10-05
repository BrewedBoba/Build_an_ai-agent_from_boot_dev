
import os

from config import MAX_CHAR


def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_path, file_path))
        valid_target_path = os.path.commonpath([working_dir_path, target_path]) == working_dir_path
        if valid_target_path == False:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, 'r') as file:
            content = file.read(MAX_CHAR)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
            return content
    except Exception as e:
        return f'Error: {str(e)}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get the content of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file where to get the contents from, relative to the working directory"
                }
            }
        }
    }
}
