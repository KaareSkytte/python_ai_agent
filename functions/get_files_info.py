import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    fullPath = os.path.join(working_directory, directory)
    
    if not os.path.abspath(fullPath).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(fullPath):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(fullPath)

        returnVal = ""

        for content in contents:
            fileName = content
            fileSize = os.path.getsize(os.path.join(fullPath, content))
            isDir = os.path.isdir(os.path.join(fullPath, content))
            returnVal = returnVal + f" - {fileName}: file_size={fileSize} bytes, is_dir={isDir}\n"
    except Exception as e:
        return f"Error: {str(e)}"
    return returnVal

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