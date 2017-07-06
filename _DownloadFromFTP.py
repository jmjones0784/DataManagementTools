#Importing System Modules
import arcpy, shutil, os, traceback, sys, logging, time, zipfile, re, urllib, ftplib
from arcpy import env


#Get working directory and create input and output paths
ftp = r''                                                                       #Input FTP Site
ftpSplit = ftp.split('.gov')                                                    #Splits FTP site into root and working directory
ftpRoot = ftpSplit[0] + '.gov'                                                  #Root FTP Site
ftpRootSite = ftpRoot[7:]                                                       #Base FTP Site, used to log in to FTP Site
workingDir = ftpSplit[1]                                                        #Working directory of FTP site, scanned for files and subsequent download
ftpPath = ftpRoot + workingDir

dlDir = r'\\geofiler\Raster\New_Raster_To_Be_Filed\3dPPC'                       #Directory where data will be downloaded into

#List

dlZip = []                                                                      #List of Downloaded Files

def exitScript():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msg)
    print pymsg
    print msg
    logging.info(pymsg)
    logging.info(msg)
    exit


if __name__ == '__main__':
    try:

        print("Starting Sync at " + time.strftime("%c"))
        arcpy.AddMessage("Starting Sync at " + time.strftime("%c"))

        #Checks the FTP site for new data

        ##ftp = ftplib.FTP('ftp.geoint.nga.ic.gov')
        ftp = ftplib.FTP(ftpRootSite)
        ftp.login()

        print "Downloading Data from " + ftpPath
        arcpy.AddMessage("Downloading Data from " + ftpPath)

        listing = []

        print "Changing Working Directory on the FTP Site to:  " + workingDir
        arcpy.AddMessage("Changing Working Directory on the FTP Site to:  " + workingDir)

        ftp.cwd(workingDir)                                                                  #Changes the working directory to the appropriate folder
        ftp.retrlines('LIST', listing.append)                                                #List all of the contents

        for item in listing:

                fileName = item.split()[8]                                                  #Gets the individual files in the folder on the FTP site
                print fileName
                zipFileName = os.path.join(dlDir, fileName)

                zipfile.ZipFile(zipFileName, mode='w')                                      #Creates a destination Zip File

                print "Created " + zipFileName
                arcpy.AddMessage("Created " + zipFileName)


                ##Downloads the appropriate ZIP file from the FTP site into the Temp Directory

                lf = open(zipFileName, "wb")
                ftp.retrbinary("RETR " + fileName, lf.write, 8*1024)
                lf.close()

                dlZip.append(zipFileName)

                print "Finished copy of " + fileName + " at " + time.strftime("%c")
                arcpy.AddMessage("Finished copy of " + fileName + " at " + time.strftime("%c"))

        ftp.quit()

    except:
        exitScript()

    finally:
        print "Copied " + str(len(dlZip)) + " files. "
        arcpy.AddMessage("Copied " + str(len(dlZip)) + " files. ")
        print("Finished Sync at " + time.strftime("%c"))
        arcpy.AddMessage("Finished Sync at " + time.strftime("%c"))
