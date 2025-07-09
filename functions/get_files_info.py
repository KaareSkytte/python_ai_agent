import os

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