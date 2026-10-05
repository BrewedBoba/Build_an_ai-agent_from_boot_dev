import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_path, file_path))

        valid_target_path = os.path.commonpath([working_dir_path, target_dir]) == working_dir_path

        if valid_target_path == False:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        with open(target_dir, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}\n'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file where to write the content, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write in a given file path"
                }
            }
        }
    }
}
