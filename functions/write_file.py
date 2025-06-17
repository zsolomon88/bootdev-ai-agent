import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        if (file_path.startswith("/")):
            abs_file_path = file_path
        else:
            abs_file_path = f'{abs_working_directory}/{file_path}'

        abs_file_path = os.path.abspath(abs_file_path)
        in_working_dir = abs_file_path.startswith(abs_working_directory)
        if (in_working_dir == False):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if (os.path.exists(os.path.dirname(abs_file_path)) == False):
            os.makedirs(os.path.dirname(abs_file_path))

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)' 

    except Exception as e:
        return f'Error: {str(e)}'