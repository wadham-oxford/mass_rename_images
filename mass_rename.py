from os import rename, listdir, startfile
from os.path import join, isdir
from tkinter import filedialog
from time import sleep
from extensions import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS

PermissionErrorFlag = False
OSErrorFlag = False


def get_extension(file_name):
    ''' Returns file extension from original file name.
        Ensures that the file extension survives name change.'''
    dot = "."
    sub_strings = file_name.split(dot)
    extension = dot + sub_strings[-1]
    return extension


def count_powers_of_ten(num):
    power = 1
    while num > 10 ** power:
        power += 1
    
    return power - 1


def get_number(x, powers):
    ''' Returns the correctly formatted number to insert into
        beginning of new file name.'''

    char = (str(x))
    powers_reduced = powers
    while x < 10 ** powers_reduced:
        powers_reduced -= 1
    
    num_zeros = powers - powers_reduced
    zeros = "0" * num_zeros
    result = f"{zeros}{char}_"
    
    return result
    

def change_names(folder_path, file_list, powers, content):
    ''' Tries to change name of every file in provided file list to
        include provided content.'''
    
    x = 1
    for file in file_list:
        try:
            original = join(folder_path, file)

            # do not change names of any subdirectories
            if not isdir(original):

                # do not change names of any files with more than one "."
                if file.count(".") < 2:

                    # check if file is an image or video file      
                    extension = get_extension(file).lower()                
                    if extension in IMAGE_EXTENSIONS or \
                    extension in VIDEO_EXTENSIONS:
                        
                        # construct new name
                        number = get_number(x, powers)
                        new_file_name = number + content + extension
                        new_path = join(folder_path, new_file_name)
                    
                        # apply new name
                        rename(original, new_path)
                        x += 1

        except FileExistsError:
            pass

        except PermissionError:
            global PermissionErrorFlag
            PermissionErrorFlag = True

        except OSError:
            global OSErrorFlag
            OSErrorFlag = True


def get_input():
    ''' Gets user to select folder where name changes will happen,
        and the string to insert into every new file name.'''
    
    while True:
        divider = "-----------------------------------------------------------"
        print("")
        print(divider)
        print(divider)
        print("MASS RENAMING TOOL")
        
        print("\nSelect folder where you want to change file names.")
        sleep(1)

        # get folder to work with
        folder_path = filedialog.askdirectory()

        # check if folder path is not empty
        if len(folder_path) > 0: 
            print("\nFolder: {}".format(folder_path))

            # check folder has files inside
            file_list = listdir(folder_path)
            num_files = len(file_list)
            if num_files > 0:
                powers = count_powers_of_ten(num_files)
                
                # get new name content from user
                content = input("\nWhat text would you like " + \
                    "all file names in this folder to include?\n\n")
                
                content_formatted = content.replace(" ", "_")
                print(f"\nContent: {content_formatted}")

                # apply name change
                change_names(folder_path, file_list, powers, content_formatted)
                
                # check if any errors arose
                if PermissionErrorFlag or OSErrorFlag: 
                    print("\nERROR: Some names could not be changed.")
                    print("\nAvoid using special characters and ensure " + \
                        "the folder or files are not open in another " + \
                        "programme.")
                else:
                    print("\nAll file names changed.")

                # open folder where name changes have occurred
                startfile(folder_path)
                print("")

                # prompt to begin loop again
                input("Press ENTER to work on another folder. ")
            
            else:
                print("\nFolder is either empty or contains too many files.")
                sleep(1)
                break
        
        else:
            print("\nNo valid folder selected.")
            sleep(1)
            break


if __name__ == "__main__":
    get_input()