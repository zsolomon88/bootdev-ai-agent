import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        if (file_path.startswith("/")):
            abs_file_path = file_path
        else:
            abs_file_path = f'{abs_working_directory}/{file_path}'

        abs_file_path = os.path.abspath(abs_file_path)
        in_working_dir = abs_file_path.startswith(abs_working_directory)
        if (in_working_dir == False):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if (os.path.exists(abs_file_path) == False):
            return f'Error: File "{file_path}" not found.'
        
        if (abs_file_path.endswith(".py") == False):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            result = subprocess.run(["python3", abs_file_path], capture_output=True, text=True, check=True, timeout=30, cwd=abs_working_directory)
            if (result.stdout == None and result.stderr == None):
                return 'No output produced.'
            result_str = f'STDOUT:{result.stdout}'
            result_str = f'{result_str}\nSTDERR:{result.stderr}'

            if (result.returncode != 0):
                result_str = f'{result_str}\nProcess exited with code {result.returncode}'

            return result_str
        except Exception as e:
            return f'Error: executing Python file: {e}'


    except Exception as e:
        return f'Error: {str(e)}'

