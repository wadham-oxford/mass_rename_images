import os
from tkinter import filedialog
from time import sleep


def get_extension(string):
    dot = "."
    sub_strings = string.split(dot)
    extension = dot + sub_strings[-1]
    return extension


def get_number(x):
    if x < 10:
        return "0{}_".format(str(x))
    else:
        return "{}_".format(str(x))
    

def change_names(folder_path, content):
    file_list = os.listdir(folder_path)
    x = 1
    for file in file_list:
        original = os.path.join(folder_path, file)
        if not os.path.isdir(original):
            number = get_number(x)
            extension = get_extension(file)
            new_file_name = number + content + extension
            new_path = os.path.join(folder_path, new_file_name)
        
            os.rename(original, new_path)
            x += 1


if __name__ == "__main__":
    while True:
        print("\n--Mass Re-Naming Tool--")
        
        print("\nSelect folder where you want to change file names.")
        sleep(1)
        folder_path = filedialog.askdirectory()

        if len(folder_path) > 0: 
            print("\nFolder: {}".format(folder_path))
            content = input("\nWhat text would you like all file names in this folder to include? ")
            print("\nContent: {}".format(content))

            change_names(folder_path, content)
            print("\nAll file names changed.")

            os.startfile(folder_path)
            print("")
            confirm = input("Press ENTER to work on another folder. ")
        
        else:
            print("\nProcess terminated.")
            sleep(1)
            break