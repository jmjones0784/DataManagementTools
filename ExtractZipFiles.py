#Importing System Modules
import arcpy, shutil, os, traceback, sys, logging, time, zipfile, re
from arcpy import env

def exitScript():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msg)
    print pymsg
    print msg
    exit

def extractZip(tempDir):
    try:
        print("Started unzipping files at... " + time.strftime("%c"))
        arcpy.AddMessage("Started unzipping files at... " + time.strftime("%c"))
        for root, dirs, files in os.walk(tempDir):
            for file in files:
                if file.endswith(".zip"):
                    zFilePath = os.path.join(root, file)
                    with zipfile.ZipFile(zFilePath, "r") as z:
                        namePath = os.path.splitext(zFilePath)[0]
                        fullPath = os.path.join(tempDir, namePath)
                        z.extractall(fullPath)

        print("Finished unzipping files at... " + time.strftime("%c"))
        arcpy.AddMessage("Finished unzipping files at... " + time.strftime("%c"))


    except:
        exitScript()


if __name__ == '__main__':

    tempDir = arcpy.GetParameterAsText(0)
##    tempDir = r'D:\GPR Holdings'

    extractZip(tempDir)