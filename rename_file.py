import os
import time
from datetime import datetime
# Import the Image module to get exif data from an image. This is a separate module that must be downloaded
# in addition to python. Read the README.txt file for download instructions
# PIL = Python Imaging Library
# EXIF = Exchangeable Image File
from PIL import Image

class rename_file:

    def __init__(self):
        print("")

    # This method receives an image file.
    # This method returns a file's date and time in a human-readable format.
    # Extracts the date and time from the file's metadata and converts it into
    # human-readable format
    def getImageDateTime(self, file):

        # Open the image
        img = Image.open(file)

        # Extract the exif data from image. Returns a dictionary of exif data
        exifinfo = img._getexif()

        try:
            # Extract the date and time taken from the exif dictionary data.
            # If you look at the raw exifinfo data, 36867 is the dictionary ID of the image date
            # Returns a string
            # Example in this format: 2020:03:26 11:35:31
            strImageDate = exifinfo[36867]

            # Parse the string and convert it to a struct_time object so python can use it.
            # The struct_time format has to be %Y:%m:%d %H:%M:%S. This is case-sensitive.
            # Returns a time_struct
            # If you look at a raw dateTimeObj struct_time it would look like:
            # time.struct_time(tm_year=2020, tm_mon=3, tm_mday=26, tm_hour=11, tm_min=35, tm_sec=31, tm_wday=3, tm_yday=86, tm_isdst=-1)
            dateTimeObj = time.strptime(strImageDate, "%Y:%m:%d %H:%M:%S")

            # Convert the struct_time object into a string as specified by the format.
            # Returns a string
            dateTime = time.strftime("%Y-%m-%d_%H.%M.%S", dateTimeObj)
        
            return dateTime

        except:
            print("The " + file + " has no date taken exif data.")
            # Get the modified time from the file metadata
            rawDateTime = os.path.getmtime(file)

            # Convert the raw datetime into a human-readable format
            dateTime = datetime.fromtimestamp(rawDateTime).strftime('%Y-%m-%d_%H.%M.%S')
            
            # Add a note
            modDateTime = "11_MODIFY_" + dateTime
    
        return modDateTime
    
    # This method receives a video file.
    # This method returns a file's date and time in a human-readable format.
    # Extracts the date and time from the file's metadata and converts it into
    # human-readable format
    def getVideoDateTime(self, file):

        # Get the modified time from the file metadata
        rawDateTime = os.path.getmtime(file)

        # Convert the raw datetime into a human-readable format
        dateTime = datetime.fromtimestamp(rawDateTime).strftime('%Y-%m-%d_%H.%M.%S')
        
        return dateTime

    # This method receives the filename and current directory.
    # This method returns a boolean.
    # Check if the filename already exists. 
    # If it exists return True, else return False.
    def fileExists(self, name, path):
        print("Checking file: " + name + " ...")
        for file in os.listdir(path):
            if file == name:
                print("The " + file + " already exists")
                return True

        print("The " + name + " does not exist.")
        
        return False

    # This method receives the file and incrementor.
    # This method returns an incremented filename.
    # Because this method is called when there is an already existing filename, it 
    # will add an incrementor to the filename ex. filename(1).jpg.
    def filenameIncrementor(self, date_time, file_type, inc):
        
        # Extract the file's date and time
        #dateTime = getDateTime(file)

        # Extract the file's file type 
        #filetype = os.path.splitext(file)[1]

        # Name the file with the datetime plus the incrementor.
        # Example: 2018-02-06_22.59.42.jpg converts to 2018-02-06_22.59.42(1).jpg
        filename = date_time + "(" + str(inc) + ")" + file_type

        print("Renaming and returning filename to: " + filename)
        return filename

    # This method receives a directory path.
    # This method will traverse through all the files in the directory and rename them
    # according to their modified date and time.
    # This method will also check for duplicated filenames and append incrementors to 
    # the filename if needed.
    def renameFiles(self, dir):
        
        # Change to directory
        os.chdir(dir)
        #print(f'dir is: {dir}')

        
        # Initially set the incrementor to 1. This variable will be used to place into
        # files that have duplicate filenames.
        incrementor = 1

        # Traverse all files in the directory
        #TODO Try using os.walk
        # https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
        for file in os.listdir(dir):

            print("Analyzing file: " + str(file))

            file_path = os.path.join(dir, file)

            if not os.path.isfile(file):
                print(f'{file} is not an acceptable file. Skipping.')
                continue

            fileType = os.path.splitext(file)[1]
            if fileType == '.MP4' or fileType == '.mp4' or fileType == '.MOV' or fileType == '.mov':
                #print(f'This is a {fileType} file')
                dateTime = self.getVideoDateTime(file)      
            else:
                #print(f'This is a {fileType} file')
                dateTime = self.getImageDateTime(file)   
            
            # Combine the file's date and time and file type to form the proposed
            # filename.
            filename = dateTime + fileType

            # Check if the file's filename is already in the correct format.
            # If it is, then skip this file and move to the next file in the directory.
            #if (filename == str(file)):
            if (filename == file):
                print("File: " + file + " is already in the correct format")
                continue
            
            # Check if filename already exists.
            # If it does, add an incrementor at the end of the name.
            #if fileExists(filename, os.getcwd()):
            if self.fileExists(filename, dir):
                
                # Add the incrementor to the file's filename
                incFilename = self.filenameIncrementor(dateTime, fileType, incrementor)            		

                # Check if the incremented filename still doesn't exist. As long as
                # the filename exists, the incrementor will increase by one for each file.
                # As long as a filename already exists in the directory, this loop will 
                # continue to increment the filename until it discovers a filename that does
                # not exist.
                # Example: 2018-02-06_22.59.42(2).jpg would become 2018-02-06_22.59.42(3).jpg
                while self.fileExists(incFilename, dir):

                    # Increase the incrementor        
                    incrementor += 1
                    
                    # Add the new incrementor to the filename.
                    incFilename = self.filenameIncrementor(dateTime, fileType, incrementor)
                    
                # Rename the file
                print("Actually Renaming: " + file + " to: " + str(incFilename))            
                os.rename(file,incFilename)            
            
            # The filename didn't exist.
            else:
                            
                print("Else Statement. Actually Renaming: " + file + " to: " + str(filename))
                os.rename(file,filename)
                
                # Reset the increment-or back to 1
                incrementor = 1