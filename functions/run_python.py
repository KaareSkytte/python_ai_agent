import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    
    complete_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(complete_file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", file_path], capture_output=True, text=True, cwd=working_directory, timeout=30,)
        stdout = result.stdout
        stderr = result.stderr
        returnCode = result.returncode
        if returnCode != 0:
            return f"STDOUT:{stdout}\nSTDERR:{stderr}\nProcess exited with code {returnCode}"
        if stdout == "" and stderr == "":
            return "No output produced."
        return f"STDOUT:{stdout}\nSTDERR:{stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    