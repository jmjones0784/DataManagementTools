import os, csv

#Arguments
src = r''
dst = r''
outFile = os.path.split(src)[1]
outFileClean = outFile.replace('-', '_')
finFile = os.path.join(dst, outFileClean) + '.csv'

#Lists
csvList = []

#Walks through a directory and identifies all CSV files
for root, dirs, files in os.walk(src):
    for file in files:
        if file.endswith(".csv"):
            csvList.append(os.path.join(root,file))

with open(finFile, 'wb') as a:
    for c in csvList:
        file = os.path.split(c)[1]
        batch = c.split('\\')[9]
        print batch
        with open(c, 'rb') as f:
            reader = csv.reader(f)
            writer = csv.writer(a)
            for row in reader:
                iRow = []
                iRow.append(batch)
                iRow.append(file)
                for i in row:
                    iRow.append(i)

                print iRow


