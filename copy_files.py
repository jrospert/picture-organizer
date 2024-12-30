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
            # default shutil.copytree syntax:
            #   shutil.copytree (src,dst,symlinks=False,ignore=None,copy_function=copy2,ignore_dangling_symlinks=False)
            #   By default, copytree uses shutil.copy2() as the copy function, which retains exif data
            # shutil.ignore_patterns will not copy file types listed in the function
            try:
                print(f'Copying folders from [{source}] to [{destination}], excluding AAE and GIF file types.')
                shutil.copytree(
                    source,
                    destination,
                    ignore = shutil.ignore_patterns('*.AAE', '*.GIF')
                )
                print(f'Successfully copied from [{source}] to [{destination}]')
            except FileExistsError:
                print(f'WARNING: The folder [{destination}] already exists. Not copying')
            except Exception as e:
                print(f'An error occurred: {e}')       