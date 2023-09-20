import os

def extract_command_msg(user_msg: str, command: str) -> str:
    full_msg = user_msg.replace(command, " ").strip()

    return full_msg


def is_valid_url(url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return True
    
def delete_file(file_path:str, file_extension=".jpg"):
    os.remove(f"{file_path}{file_extension}")
    print("file deleted")




def delete_all_files(directory="./", file_extension=".jpg"):
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            os.remove(os.path.join(directory, filename))
    print(f"All {file_extension} files deleted")



def list_files(directory="./"):
    for filename in os.listdir(directory):
        print(filename)



