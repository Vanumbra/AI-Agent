import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:

        working_directory_absolute = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_absolute, directory))
        valid_target_directory = os.path.commonpath([working_directory_absolute, target_directory]) == working_directory_absolute

        if valid_target_directory is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            lines.append(f" - {item}: file_size={file_size} bytes, is_dir={is_directory}")
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}    