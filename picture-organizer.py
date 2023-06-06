###########################################
##          Picture Organizer 1.0        ##
##                                       ##
## Author: Joel Rospert                  ##
## Date: 05/17/2020                      ##  
## Revision: 05/14/2023                  ##
###########################################

import os
import argparse
import sys
from rename_file import rename_file
from copy_files import copy_files

# Changing Directory:
# If you change directory from C:\Users\Joel\Desktop\phone\fb, then
# you only need to change the 2 'fbdir' variables below   
# 
def isFileDirExists(dir):
    return os.path.exists(dir)

def valid_args(arguments, *valid):
    args_provided= []
    for argument in arguments:
        if not argument[0] == "action" and not (
            argument[1] == None or argument[1] == False
        ):
            args_provided.append(argument[0])
    for arg_provided in args_provided:
        if not arg_provided in valid:
            return False
    return True 	

def main():
    parser = argparse.ArgumentParser(description="picture organizing tool")
    parser.add_argument(
        "action",
        choices=[
            "copy_files",
            "rename_files",
        ],
    )
    parser.add_argument("--src_dir", help="location of files to copy from")
    parser.add_argument("--dst_dir", help="location to copy files to")
    parser.add_argument("--file_dir", help="location of files to rename")
    args = parser.parse_args()
    arg_list = [(arg, getattr(args, arg)) for arg in vars(args)]

    if args.action == "copy_files":
        if not valid_args(arg_list, "src_dir", "dst_dir"):
            sys.exit("Invalid Option Provided for copy_files")
        if args.src_dir and args.dst_dir:
            srcdir = args.src_dir
            dstdir = args.dst_dir

            if not isFileDirExists(srcdir):
                sys.exit("Source file directory doesn't exist. Exiting...")
            copyFiles = copy_files()
            copyFiles.copyFiles(srcdir, dstdir)
        else:
            sys.exit("copy_files requires --src_dir and --dest_dir options")
    
    if args.action == "rename_files":
        if not valid_args(arg_list, "file_dir"):
            sys.exit("Invalid Option Provided for rename_files")
        if args.file_dir:
            filedir = args.file_dir
            #print(f'phonedir is: {filedir}')
            
            if not isFileDirExists(filedir):
                #os.makedirs(filedir, 711)
                sys.exit("File directory doesn't exist. Exiting...")
            else:
                pass

            # Change to directory to work in
            os.chdir(filedir)

            renameFiles = rename_file()
            renameFiles.renameFiles(filedir)

        else:
            sys.exit("rename_files requires --file_dir option")   
		    
	
if __name__ == "__main__":
    main()
