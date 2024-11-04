import os
from tkinter import filedialog

print("\nSelect folder where you want to change file names.")
folder_path = filedialog.askdirectory()

content = input("\nWhat text would you like to all file names in this folder to include? ")

# add way of retaining file extension
file_list = os.listdir(folder_path)
x = 1
for file in file_list:
    original = os.path.join(folder_path, file)
    if x < 10:
        number = "0{}_".format(str(x))
    else:
        number = "{}_".format(str(x))
    new_file_name = number + content
    new_path = os.path.join(folder_path, new_file_name)
    os.rename(original, new_path)
    x += 1

print("\nAll file names in {} are now renamed with structure 00_{}".format(folder_path, content))
