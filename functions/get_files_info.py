import os

try:
    def get_files_info(working_directory, directory="."):

        if directory == ".":
            directory = working_directory

        abs_working_dir = os.path.abspath(working_directory)
        if not working_directory == directory:
            full_path = os.path.join(abs_working_dir, directory)
        else:
            full_path = os.path.abspath(abs_working_dir)

        # print("-------------")
        # print(abs_working_dir)
        # print(full_path)
        # print("-------------")

        if not os.path.isdir(full_path):
           return print(f'Error: "{directory}" is not a directory')
        
        if not full_path.startswith(abs_working_dir) or directory == "../":
            return print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        
        list_dir = os.listdir(full_path)

        print(f"Result for '{directory}' directory: ")
        for item in list_dir:
            item_path = os.path.join(full_path, item)

            print(f"- {item}: file_size: {os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")

except Exception as e:
    print(f"Error: {e}")