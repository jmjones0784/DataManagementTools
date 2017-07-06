import arcpy, os, time, sys, traceback
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



Datatype = "FeatureClass"
sourceFolder = arcpy.GetParameterAsText(0)

DeletedFC = 0

try:

    print("STARING SYNC AT " + time.strftime("%c"))
    arcpy.AddMessage("STARING SYNC AT " + time.strftime("%c"))

    print "Beginning discovery of relevant feature classes"
    arcpy.AddMessage("Beginning discovery of relevant feature classes")

    for dirpath, dirnames, filenames in arcpy.da.Walk(sourceFolder, Datatype, type=['Point', 'Polyline', 'Polygon']):
        for filename in filenames:
            fcToDelete = (os.path.join(dirpath, filename))
            arcpy.Delete_management(fcToDelete)
            DeletedFC += 1

    print "Found and deleted" + str(DeletedFC) + " feature classes"
    arcpy.AddMessage("Found and deleted" + str(DeletedFC) + " feature classes")

except:
        exitScript()

finally:

    print("FINISHED SCRIPT AT " + time.strftime("%c"))
    arcpy.AddMessage("FINISHED SCRIPT AT " + time.strftime("%c"))