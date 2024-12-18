import os
from tkinter import filedialog
from time import sleep
from extensions import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS

MAX_NUM_FILES = 999

PermissionErrorFlag = False
OSErrorFlag = False

def get_extension(string):
    ''' Returns file extension from original file name.
        Ensures that the file extension survives name change.'''
    dot = "."
    sub_strings = string.split(dot)
    extension = dot + sub_strings[-1]
    return extension


def get_number(x):
    ''' Returns the correctly formatted number to insert into
        beginning of new file name.'''
    char = (str(x))
    if num_files < 100:
        if x < 10:
            return "0{}_".format(char)
        else:
            return "{}_".format(char)
    elif num_files >= 100:
        if x < 10:
            return "00{}_".format(char)
        elif x < 100:
            return "0{}_".format(char)
        else:
            return "{}_".format(char)
    

def change_names(folder_path, file_list, content):
    ''' Tries to change name of every file in provided file list to
        include provided content.'''
    
    x = 1
    for file in file_list:
        try:
            original = os.path.join(folder_path, file)

            # do not change names of any subdirectories
            if not os.path.isdir(original):

                # do not change names of any files with more than one "."
                periods = []
                for char in file:
                    if char == ".":
                        periods.append(char) 
                if len(periods) < 2:

                    # check if file is in an image or video file      
                    extension = get_extension(file)
                    extension_formatted = extension.lower()                    
                    if extension_formatted in IMAGE_EXTENSIONS or \
                    extension_formatted in VIDEO_EXTENSIONS:
                        
                        # construct new name
                        number = get_number(x)
                        new_file_name = number + content + extension
                        new_path = os.path.join(folder_path, new_file_name)
                    
                        # apply new name
                        os.rename(original, new_path)
                        x += 1

        except FileExistsError:
            pass

        except PermissionError:
            global PermissionErrorFlag
            PermissionErrorFlag = True

        except OSError:
            global OSErrorFlag
            OSErrorFlag = True


if __name__ == "__main__":
    while True:
        print("\n--Mass Re-Naming Tool--")
        
        print("\nSelect folder where you want to change file names.")
        sleep(1)

        # get folder to work with
        folder_path = filedialog.askdirectory()

        # check if folder path is not empty
        if len(folder_path) > 0: 
            print("\nFolder: {}".format(folder_path))

            # check if number of files is within accepted limit
            file_list = os.listdir(folder_path)
            global num_files
            num_files = len(file_list)
            if num_files > 0 and num_files <= MAX_NUM_FILES:

                # get new name content from user
                content = input("\nWhat text would you like " + \
                    "all file names in this folder to include?\n\n")
                
                content_formatted = content.replace(" ", "_")
                print("\nContent: {}".format(content_formatted))

                # apply name change
                change_names(folder_path, file_list, content_formatted)
                
                # check if any errors arose
                if PermissionErrorFlag or OSErrorFlag: 
                    print("\nERROR: Some names could not be changed.")
                    print("\nAvoid using special characters and ensure " + \
                        "the folder or files are not open in another " + \
                        "programme.")
                else:
                    print("\nAll file names changed.")

                # open folder where name changes have occurred
                os.startfile(folder_path)
                print("")

                # prompt to begin loop again
                confirm = input("Press ENTER to work on another folder. ")
            
            else:
                print("\nFolder is either empty or contains too many files.")
                sleep(1)
                break
        
        else:
            print("\nNo valid folder selected.")
            sleep(1)
            break