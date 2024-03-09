# HW2 - Ranking Webpages
### Justin Jenkins
### CS 432, Spring 2024
### Mar 8, 2024 (extended)

# Q1

*For the following tasks, consider which items could be scripted, either with a shell script or with Python.  You may even want to create separate scripts for different tasks.  It's up to you to determine the best way to collect the data.*

Download the HTML content of the 500 unique URIs you gathered in HW1 and strip out HTML tags (called "boilerplate") so that you are left with the main text content of each webpage.  ***Plan ahead because this will take time to complete.***

Note: If you plan completing this question in Windows PowerShell (instead of Linux), you will need to be aware of how PowerShell [uses character encoding for string data](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.1) (see also [Understanding file encoding in VS Code and PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/dev-cross-plat/vscode/understanding-file-encoding?view=powershell-7.1)).

#### Saving the HTML Files

We just want to save the HTML content.  In Python, we can use the [requests library](https://requests.readthedocs.io/en/latest/) to download the webpage. Once the webpage has been successfully requested, the [HTML response content can be accessed using the `text` property](https://requests.readthedocs.io/en/latest/user/quickstart/#response-content).

You'll need to save the HTML content returned from each URI in a uniquely-named file.  The easiest thing is to use the URI itself as the filename, but your shell will likely not like some of the characters that can occur in URIs (e.g., "?", "&").  My suggestion is to hash the URIs to associate them with their respective filename using a [cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function), like MD5.  

For example, https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21 hashes to `2fc5f9f05c7a69c6d658eb680c7fa6ee`:
```console
$ echo -n "https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21" | md5sum | awk '{print $1}'
2fc5f9f05c7a69c6d658eb680c7fa6ee
```
Notes:
* `md5sum` might be `md5` on some machines
* note the `-n` option to `echo` -- this removes the trailing newline
* `awk '{print $1}'` at the end prints only the characters before the first space in the output (i.e., the hash) -- *try the command without this to see the difference*

If you want to use Python for this, you can use the [hashlib library](https://docs.python.org/3/library/hashlib.html). Note that you'll want to strip any trailing whitespace or newline characters from the URI (using [`strip()`](https://www.w3schools.com/python/ref_string_strip.asp)) before you compute the MD5 hash.

For later analysis, you will need to map the content back to the original URI, so make sure to save a text file that contains all of the URI to hash mappings.

#### Removing HTML Boilerplate

Now use a tool to remove (most) of the HTML markup from your 500 HTML documents. 

The Python boilerpy3 library will do a fair job at this task.  You can use `pip` to install this Python package in your account on the CS Linux machines.  The [main boilerpy3 webpage](https://pypi.org/project/boilerpy3/) has several examples of its usage.

Keep both files for each URI (i.e., raw HTML and processed), and upload both sets of files to your GitHub repo. Put the raw and processed files in separate folders.  Remember that to upload/commit a large number of files to GitHub, [use the command line](https://docs.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository-using-the-command-line).

Sometimes boilerpy3 isn't able to extract any useful information from the downloaded HTML (either it's all boilerplate or it's not actually HTML), so it produces no output, resulting in a 0B size file.  You may also run into HTML files that trigger UnicodeDecode exceptions when using boilerpy3.  You can skip files that have  these types of encoding errors, result in 0B output, or contain inappropriate content (whatever you define as such).  The main goal is to have enough processed files so that you can find 10 documents that contain your query term (for Q2 and later).

*Q: How many of your 500 URIs produced useful text?  If that number was less than 500, did that surprise you?* 

## Answer

After attempting to download all the raw HTML files, I was left with only 357 .html files. Following which it dropped down to 351 'boiled' files, including numerous with useless information or empty files. I am not particularly suprised by this. Included is an example of a useless but not empty .html file after the boilerplate content was removed.

![\label{fig:web-growth}](uselessInfo.png)

This makes sense to me as many links will contain small things meant for specific or small purposes, many do not have the purpose of conveying information but instead giving functionality that will be removed when we filter out boilerplate content.
I converted all the names of files to md5sum as suggested and further converted the content to hexadecimal with .hexdigest(). To remove boilerplate content I also followed the suggestion of boilerpy3.

code without comments, used a main function to run everything.
```
def main():
    linksFile = open("links.txt", 'r')
    for uRI in linksFile:
        uRI = uRI.strip()
        filename = md5Name(uRI)
        downloadFile(uRI, filename)
    boilFile()
    
def md5Name(uRI):
    hashed = hashlib.md5(uRI.encode())

    md5map = open("md5_to_URI.txt", 'a')
    md5map.write(hashed.hexdigest() + " = " + uRI + "\n")
    md5map.close()

    return hashed.hexdigest() + ".html"

def downloadFile(uRI, filename):
    try:
        response = requests.get(uRI)
        if response.status_code == 200:
            filepath = f"./CS432_HW2/RawFiles/{filename}"
            file = open (filepath, 'w')
            file.write(response.text)
            file.close()

    except Exception as error:
        print(f"Error from url  {uRI}:\n {error}")

def boilFile() : 
    
    boiler = extractors.ArticleExtractor()

    for rawFile in os.listdir("./CS432_HW2/RawFiles") : 
        filePath = f"./CS432_HW2/RawFiles/{rawFile}"
        boiledFilePath = f"./CS432_HW2/ProcessedFiles/{rawFile}"
        try: 
            file = open(filePath, 'r')
            html = file.read()
            file.close()
            
            boiledContent = boiler.get_content(html)

            boiledFile = open(boiledFilePath, 'w')
            boiledFile.write(boiledContent)
            boiledFile.close()

        except Exception as error:
            print(f"Error at {filePath}: {error}")
```



# Q2
Choose a query term (e.g., "coronavirus") that is not a stop word (e.g, "the"), not super-general (e.g., "web"), and not used in HTML markup (e.g., "http") that is found in at least 10 of your documents.  If the term is present in more than 10 documents, choose any 10 **English-language** documents from *different domains* from the result set.  (Hint: You may want to use the Unix command `grep -c` on the processed files to help identify a good query -- it indicates the number of lines where the query appears.) 

As per the example in the [Searching the Web slides](https://docs.google.com/presentation/d/1xHWYidHcqPljtvqcGsUXgXU7j6KEFDVXrTftHmkv6OA/edit?usp=sharing), compute TF-IDF values for the query term in each of the 10 documents and create a table with the TF, IDF, and TF-IDF values, as well as the corresponding URIs. (If you are using LaTeX, you should create a [LaTeX table](https://www.overleaf.com/learn/latex/tables).  If you are using Markdown, view the raw version of this file for an example of how to generate a table.) Rank the URIs in decreasing order by TF-IDF values.  For example:

Table 1. 10 Hits for the term "shadow", ranked by TF-IDF.

|TF-IDF	|TF	|IDF	|URI
|------:|--:|---:|---
|0.150	|0.014	|10.680	|http://foo.com/
|0.044	|0.008	|10.680	|http://bar.com/

You can use Google or Bing for the DF estimation:
* Google - use **40 billion** as the total size of the corpus
* Bing - use **4 billion** as the total size of the corpus

*These numbers are based on data from <https://www.worldwidewebsize.com>.*

To count the number of words in the processed document (i.e., the denominator for TF), you can use the Unix command `wc`:

```console
% wc -w 2fc5f9f05c7a69c6d658eb680c7fa6ee.txt
    19261 2fc5f9f05c7a69c6d658eb680c7fa6ee.txt
```
It won't be completely accurate, but it will be probably be consistently inaccurate across all files.  You can use more 
accurate methods if you'd like, just explain how you did it.  

Don't forget the log base 2 for IDF, and mind your [significant digits](https://en.wikipedia.org/wiki/Significant_figures#Rounding_and_decimal_places).

*You must discuss in your report how you computed the values (especially IDF) and provide the formulas you used for TF, IDF, and TF-IDF.*  

## Answer
For this question I used the term 'device', I found my results with a small python script here:
```
import os

searchTerm = "device"
folder = "./CS432_HW2/ProcessedFiles"
searchFound = {}

for filePath in os.listdir(folder):
    file = open(f"./CS432_HW2/ProcessedFiles/{filePath}")
    content = file.read()
    content = content.lower()
    count = content.count(searchTerm)
    if count > 0 :
        searchFound[filePath] = count
    
if searchFound : 
    print(f"Search term: {searchTerm} \n Found in:\n")
    for filePath, count in searchFound.items():
        print(f"{filePath} | Count: {count}")
else : 
    print(f"{searchTerm} not found in files")
```
Table 1. 10 Hits for the term 'device', ranked by TF-IDF.
|TF-IDF |TF    |IDF    |URI    |term count |word count  
|------:|----:|-----:|---|-:|---:
|.0173 |.0129 |1.3383 |https://www.setf.com/ |2 |154
|.0158 |.0118 |1.3383 |https://m.me/AliExpress |4 |340
|.0096 |.0072 |1.3383 |https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Cookie_statement |4 |553
|.0079 |.0059 |1.3383 |https://tv.youtube.com/learn/nflsundayticket |10 |1702
|.0032 |.0024 |1.3383 |https://play.google.com/store/apps/details?id=com.reddit.frontpage |1 |416
|.0028 |.0017 |1.3383 |https://www.reddit.com/policies/privacy-policy |8 |4619
|.0024 |.0018 |1.3383 |https://www.chevrolet.com/accessibility |2 |1112
|.0017 |.0013 |1.3383 |https://docs.github.com/site-policy/privacy-policies/github-privacy-statement |4 |3140
|.0015 |.0011 |1.3383 |https://explore.zoom.us/en/team/ |3 |2689
|.0005 |.0004 |1.3383 |https://terms.alicdn.com/legal-agreement/terms/suit_bu1_aliexpress/suit_bu1_aliexpress202204182115_66077.html |7 |16020

To calculate these values, I grabbed the term count from my search.py and the wordcount from 'wc -w <file>' in console, I then divided the term count by the word count to calculate the tf value, example 2/154 = .0129 (setf.com)
Following this, I calculated the IDF on google for the term ('device'), receiving 15,820,000,000 results from the estimated 40,000,000,000 size of the corpus
Using Log2(40bil/15.820bil) gives the IDF result, which I multiplied with the TF for each result to receive its TF-IDF value. example .0129 * 1.3383 = .0173 (setf.com)

# Q3
Now rank the *domains* of those 10 URIs from Q2 by their PageRank.  Use any of the free PR estimators on the web,
such as:
* https://searchenginereports.net/google-pagerank-checker
* https://dnschecker.org/pagerank.php
* https://smallseotools.com/google-pagerank-checker/
* https://www.duplichecker.com/page-rank-checker.php

Note that these work best on domains, not full URIs, so, for example, submit things `https://www.cnn.com/` rather than `https://www.cnn.com/world/live-news/nasa-mars-rover-landing-02-18-21`.

If you use these tools, you'll have to do so by hand (most have anti-bot captchas), but there are only 10 to do.  

Normalize the values they give you to be from 0 to 1.0.  Use the same tool on all 10 (again, consistency is more important than accuracy). 

Create a table similar to Table 1:

Table 2.  10 hits for the term "shadow", ranked by PageRank of domain.

|PageRank	|URI
|-----:|---
|0.9|		http://bar.com/
|0.5	|	http://foo.com/

*Q: Briefly compare and contrast the rankings produced in Q2 and Q3.*
## Answer
To calculate these I used <https://dnschecker.org/pagerank.php>, I took each URI and concatenated it to its extension. The results received rank from 1 to 10 so I divided the results by 10 to scale them from 0 to 1. (two exceptions to this was https://play.google.com/store/apps/details?id=com.reddit.frontpage, and https://m.me/AliExpress, as they both are advertising their service on another website, and I figure its more accurate to to keep the extension in. Please let me know if this was incorrect)
|PageRank	|URI
|-----:|---
|0.9 |https://play.google.com/store/apps/details?id=com.reddit.frontpage
|0.8 |https://www.reddit.com
|0.6 |https://explore.zoom.us		
|0.6 |https://tv.youtube.com
|0.6 |https://m.me/AliExpress
|0.6 |https://docs.github.com/
|0.5 |https://www.chevrolet.com
|0.5 |https://foundation.wikimedia.org
|0.5 |https://terms.alicdn.com
|0.3 |https://www.setf.com/



# References

* Python, __main__ — Top-level code environment, <https://docs.python.org/3/library/__main__.html>
* Stackoverflow, how can I iterate over files in a given directory, <https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory>
* jmriebold, boilerpy3 documentation, <https://github.com/jmriebold/BoilerPy3>
* Matthew Brett, using variables in strings, <https://matthew-brett.github.io/teaching/string_formatting.html>
* GeeksforGeeks, md5hash in python, <https://www.geeksforgeeks.org/md5-hash-python/>

