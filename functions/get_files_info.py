import os

def get_files_info(working_directory, directory=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        if directory == None:
            abs_directory = abs_working_directory
        else:
            abs_directory = f'{abs_working_directory}/{directory}'
        abs_directory = os.path.abspath(abs_directory)
        if os.path.isdir(abs_directory) == False:
            return f'Error: "{directory}" is not a directory'

        in_working_dir = abs_directory.startswith(abs_working_directory)
        if (in_working_dir == False):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        list_string = ""
        list_dir = os.listdir(path=abs_directory)
        for file in list_dir:
            file_path = f'{abs_directory}/{file}'
            list_string = f'{list_string}\n- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}'

    except Exception as e:
        return f'Error: {str(e)}'

    list_string = str.strip(list_string)
    return list_string

