import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_absolute, file_path))
        valid_target_file = os.path.commonpath([working_directory_absolute, target_file]) == working_directory_absolute

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd = working_directory_absolute,
            capture_output = True,
            text = True,
            timeout = 30,
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file as a script and returns its output. Use this when the user wants to execute, run, or launch a Python program — not just view or read its contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to be executed, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of arguments to pass to the Python file when executing it."
                }
            },
            "required": ["file_path"],
        },
    },
}  
        