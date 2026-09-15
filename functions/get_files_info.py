import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_path, directory))

        valid_target_path = os.path.commonpath([working_dir_path, target_dir]) == working_dir_path

        if valid_target_path == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        result = ""
        for file in os.listdir(target_dir):
            full_path = os.path.join(target_dir, file)
            result += f"- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}\n"
        return result

    except Exception as e:
        return f'Error: {str(e)}\n'
