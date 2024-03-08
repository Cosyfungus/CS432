import requests
import hashlib
from boilerpy3 import extractors
import os

#opens links.txt and loops through it to grab URI for other functions
def main():
    linksFile = open("links.txt", 'r')
    for uRI in linksFile:
        uRI = uRI.strip()
        filename = md5Name(uRI)
        downloadFile(uRI, filename)
    boilFile()

# converts URI to md5 and saves it with original URI       
def md5Name(uRI):
    hashed = hashlib.md5(uRI.encode())

    md5map = open("md5_to_URI.txt", 'a')
    #.hexdigest() to make the md5sum a bit nicer looking
    md5map.write(hashed.hexdigest() + " = " + uRI + "\n")
    md5map.close()

    return hashed.hexdigest() + ".html"

#download the html content from 'uRI' and save it as 'filename'
def downloadFile(uRI, filename):
    try:
        response = requests.get(uRI)
        # only tries to save the document if it receives
        # a status code of 200 indicating successful connection
        # as this is a get request 200 will work for most cases
        if response.status_code == 200:
            # creates path towards the correct folder and 
            # saves the data into that folder
            filepath = f"./CS432_HW2/RawFiles/{filename}"
            file = open (filepath, 'w')
            file.write(response.text)
            file.close()

    except Exception as error:
        print(f"Error from url  {uRI}:\n {error}")

# extracts boilerplate content from rawfiles
# saves new file it processedfiles folder
def boilFile() : 
    
    # creates boilerpy3 object to extract boilerplate content
    boiler = extractors.ArticleExtractor()

    #loops through all files in the folder
    for rawFile in os.listdir("./CS432_HW2/RawFiles") : 
        filePath = f"./CS432_HW2/RawFiles/{rawFile}"
        boiledFilePath = f"./CS432_HW2/ProcessedFiles/{rawFile}"
        try: 
            #pulls the raw html
            file = open(filePath, 'r')
            html = file.read()
            file.close()
            
            #extraction from raw html
            boiledContent = boiler.get_content(html)

            #save to new file
            boiledFile = open(boiledFilePath, 'w')
            boiledFile.write(boiledContent)
            boiledFile.close()

        except Exception as error:
            print(f"Error at {filePath}: {error}")


            
if __name__ == '__main__' :
    main()