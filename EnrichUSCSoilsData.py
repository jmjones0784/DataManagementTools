#Importing System Modules
import shutil, os, traceback, sys, time, zipfile, datetime
import csv
import arcpy
env = arcpy.env

soilDict = {"GW":"Well-graded gravels or gravel-sand mixtures - little or no fines / 0.19 - 3 / 4.75 - 75.0 / 110 - 140 / 17.5 - 22.0 / 125 - 150 / 19.5 - 23.5 / 1 - 100 / 0.03 - 3 / NA / NA / Good - pervious / Good / Almost none / Very stable / Excellent / Good / 40 - 80",
            "GP":"Poorly graded gravels or gravel-sand mixtures - little or no fines / 0.19 - 3 / 4.75 - 75.0 / 110 - 130 / 17.5 - 20.5 / 125 - 140 / 19.5 - 22.0 / 1 - 100 / 0.03 - 3 / NA / NA / Good - pervious / Good / Almost none / Reasonably stable / Excellent to good / Poor to fair / 30 - 60",
            "GM":"Silty gravels - gravel-sand-silt mixtures / 0.19 - 3 / 4.75 - 75.0 / 100 - 130 / 16.0 - 20.5 / 125 - 140 / 19.5 - 22.0 / 0.01 - 10 / 0.0003 - 0.3 / NA / NA / Poor, semi-pervious / Good / Slight / Reasonably stable / Excellent to good / Fair to poor / 20 - 60",
            "GC":"Clayey gravels - gravel-sand-clay mixtures / 0.19 - 3 / 4.75 - 75.0 / 100 - 130 / 16.0 - 20.5 / 125 - 140 / 19.5 - 22.0 / 0.01 - 10 / 0.0003 - 0.3 / NA / NA / Poor, semi-pervious / Good to Fair / Slight / Reasonably stable / Good / Good to fair - not suitable if subject frost / 20 - 40",
            "SW":"Well-graded sands or gravelly sands - little or no fines / 0.0029 - 0.19 / 0.075 - 4.75 / 95 - 135 / 15.0 - 21.0 / 120 - 145 / 19.0 - 23.0 / 0.001 - 1 / 3x10-5 - 0.03 / 0.03 - 2.0 / 0.04 - 3.5 / Good, pervious / Good / Almost none / Very stable / Good / Fair to poor / 20 - 40",
            "SP":"Poorly graded sands or gravelly sands - little or no fines / 0.0029 - 0.19 / 0.075 - 4.75 / 95 - 125 / 15.0 - 19.5 / 120 - 135 / 19.0 - 21.0 / 0.001 - 1 / 3x10-5 - 0.03 / 0.03 - 2.0 / 0.04 - 3.6 / Good, pervious / Good / Almost none / Reasonably stable when dense / Good to fair / Poor / 10 - 40",
            "SM":"Silty sands - sand-silt mixtures / 0.0029 - 0.19 / 0.075 - 4.75 / 80 - 135 / 12.5 - 21.0 / 110 - 140 / 17.5 - 22.0 / 0.001 - 0.01 / 3x10-5 - 0.0003 / 0.03 - 2.0 / 0.04 - 3.7 / Poor - impervious / Good / Slight / Reasonably stable when dense / Good to fair / Poor / 10 - 40",
            "SC":"Clayey sands - sand-silt mixtures / 0.0029 - 0.19 / 0.075 - 4.75 / 85 - 130 / 13.5 - 20.5 / 110 - 135 / 17.5 - 21.0 / 0.0001 - 0.01 / 3x10-6 - 0.0003 / 0.03 - 2.0 / 0.04 - 3.8 / Poor - impervious / Good to Fair / Slight to medium / Reasonably stable / Good to fair / Fair to poor - not suitable if subject to frost / 5 - 20",
            "M":"Inorganic silts with very fine sands - rock flour - silty or clayey fine sands or clayey silts with slight plasticity / < 0.0032 / < 0.075 / 75 - 110 / 11.5 - 17.5 / 75 - 130 / 11.5 - 20.5 / 10-8 - 0.001 / 3x10-10 - 3x10-5 / 1.5 - 10 / 2.5 - 12 / Poor, impervious / Good to Poor / Slight to high / Fair stability - good compaction required / Fair to poor / Not suitable / 15 or less",
            "C":"Inorganic clays of plasticity - fat clays / < 0.0033 / < 0.075 / 80 - 110 / 12.5 - 17.5 / 70 - 125 / 11.0 - 19.5 / 10-10 - 10-6 / 3x10-12 - 3x10-8 / >= 10 / >= 10 / No drainage - impervious / Good to Poor / Medium to very high / Fair to good stability - expands - weakens - shrinks - cracks / Fair to very poor / Not suitable / 15 or less",
            "N/A":"NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA",
            "NoData":"NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA / NA"}

fields = ["USC_DESIG", "Desc_", "ASTMin", "ASTMm", "UWAlf", "UWAkNm", "UWUlf", "UWUkNm", "HydConCmS", "HydConFtS", "AHCRmLS", "AHCRmDS", "Drain", "Compact", "CompExp", "ValueFill", "ValuePave", "ValueBC", "CBR"]
logPath = r'\\geofiler\Data_Archive\ProcessingLogs\Soils'

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

if __name__ == '__main__':

    outFile = 'Update_USC_Tables' + str(datetime.datetime.today()) + '.txt'
    fileFixed = outFile.replace(':', '-')
    outFilePath = os.path.join(logPath, fileFixed)

    with open(outFilePath, mode="w") as newfile:

        sourceFC = arcpy.GetParameterAsText(0)
        addFields = arcpy.GetParameterAsText(1)

        result = arcpy.GetCount_management(sourceFC)
        fcCount = int(result.getOutput(0))

        print("STARING SYNC AT " + time.strftime("%c"))
        newfile.write("STARING SYNC AT " + time.strftime("%c") + '\n')
        arcpy.AddMessage("STARING SYNC AT " + time.strftime("%c"))

        try:

            if addFields == "Yes":

                print("Adding Relevant Fields at " + time.strftime("%c"))
                newfile.write("Adding Relevant Fields at " + time.strftime("%c"))
                arcpy.AddMessage("Adding Relevant Fields at " + time.strftime("%c"))

                arcpy.AddField_management(sourceFC, "Desc", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "ASTMin", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "ASTMm", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "UWAlf", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "UWAkNm", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "UWUlf", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "UWUkNm", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "HydConCmS", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "HydConFtS", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "AHCRmLS", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "AHCRmDS", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "Drain", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "Compact", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "CompExp", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "ValueFill", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "ValuePave", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "ValueBC", "TEXT", "", "", "500")

                arcpy.AddField_management(sourceFC, "CBR", "TEXT", "", "", "500")

                print("Successfully added Relevant Fields at " + time.strftime("%c"))
                newfile.write("Successfully added Relevant Fields at " + time.strftime("%c"))
                arcpy.AddMessage("Successfully added Relevant Fields at " + time.strftime("%c"))

            uCursor = arcpy.da.UpdateCursor(sourceFC, fields)

            print("Beginning update at " + time.strftime("%c"))
            newfile.write("Beginning update at " + time.strftime("%c"))
            arcpy.AddMessage("Beginning update at " + time.strftime("%c"))

            rowCount = 0

            for row in uCursor:

                update = soilDict[row[0]].split("/")

                row[1] = update[0]
                row[2] = update[1]
                row[3] = update[2]
                row[4] = update[3]
                row[5] = update[4]
                row[6] = update[5]
                row[7] = update[6]
                row[8] = update[7]
                row[9] = update[8]
                row[10] = update[9]
                row[11] = update[10]
                row[12] = update[11]
                row[13] = update[12]
                row[14] = update[13]
                row[15] = update[14]
                row[16] = update[15]
                row[17] = update[16]
                row[18] = update[17]

                uCursor.updateRow(row)

                rowCount += 1

                if rowCount % 1000 == 0:
                    print("Completed " + str(rowCount) + " out of " + str(fcCount) + " rows...")
                    arcpy.AddMessage("Completed " + str(rowCount) + " out of " + str(fcCount) + " rows...")


        except:
            exitScript()

        finally:
            print("FINISHED SYNC AT " + time.strftime("%c"))
            arcpy.AddMessage("FINISHED SYNC AT " + time.strftime("%c"))
            newfile.write("FINISHED SYNC AT " + time.strftime("%c") + '\n')