import os

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        if (file_path.startswith("/")):
            abs_file_path = file_path
        else:
            abs_file_path = f'{abs_working_directory}/{file_path}'

        abs_file_path = os.path.abspath(abs_file_path)
        in_working_dir = abs_file_path.startswith(abs_working_directory)
        if (in_working_dir == False):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if (os.path.isfile(abs_file_path) == False):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) >= MAX_CHARS:
            file_content_string = f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string

    except Exception as e:
        return f'Error: {str(e)}'