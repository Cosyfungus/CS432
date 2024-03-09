import os

searchTerm = "device"
folder = "./CS432_HW2/ProcessedFiles"
searchFound = {}

for filePath in os.listdir(folder):
    file = open(f"./CS432_HW2/ProcessedFiles/{filePath}")
    content = file.read()
    content = content.lower()
    #counts every instance of the search term in the document
    count = content.count(searchTerm)
    if count > 0 :
        searchFound[filePath] = count
    
if searchFound : 
    print(f"Search term: {searchTerm} \n Found in:\n")
    for filePath, count in searchFound.items():
        print(f"{filePath} | Count: {count}")
else : 
    print(f"{searchTerm} not found in files")