import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_path, file_path))

        valid_target_path = os.path.commonpath([working_dir_path, target_dir]) == working_dir_path

        if valid_target_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_dir_path, capture_output=True, text=True, timeout=30)

        output = []

        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            output.append('No output produced')
        if result.stdout:
            output.append(f'STDOUT:{result.stdout}')
        if result.stderr:
            output.append(f'STDERR:{result.stderr}')
        return '\n'.join(output)
    except Exception as e:
        return f'Error: {str(e)}\n'
