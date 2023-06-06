import os
import shutil

class copy_files:

    def __init__(self):
        print("")
   
    def copyFiles(self, src, dst):

        for file in os.listdir(src):
            source = os.path.join(src, file)
            destination = os.path.join(dst,file)
            
            # shutil.copytree retains the exif data
            # default shutil.copytree syntax
            # shutil.copytree (src,dst,symlinks=False,ignore=None,copy_function=copy2,ignore_dangling_symlinks=False)
            # By default, copytree uses shutil.copy2() as the copy function, which retains exif data
            shutil.copytree(source, destination)            
           
              

        