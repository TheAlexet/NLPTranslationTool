import requests
import sys
import os
import time
import json

my_key = "4ff64d62-a732-706b-9385-34e341c61eb3:fx"
url_translate = "https://api-free.deepl.com/v2/document"
url_status = "https://api-free.deepl.com/v2/document/{0}"
url_result = "https://api-free.deepl.com/v2/document/{0}/result"
source_language = "EN"
target_language = "ES"

#The file is translated using the DeepL API.
#The resulting document's id and key are provided as a response.
def translate(path):
    up_file = open(path,"rb")
    _params = {
        "source_lang" : source_language,
        "auth_key" : my_key,
        "target_lang" : target_language
    }
    response = requests.post(url_translate,params=_params,files={"file":up_file})
    json_response = json.loads(response.text)
    id = json_response["document_id"]
    key = json_response["document_key"]
    print("Waiting for translation...")
    time.sleep(5)
    check_status(id, key)

#Using the document's id and key obtained, the translation status is checked.
def check_status(id, key):
    _params = {
        "auth_key" : my_key,
        "document_key" : key
    }
    response = requests.get(url_status.format(id),params=_params)
    print("Translation done!")
    print(response.text)
    get_result(id, key)

#Using the document's id and key obtained, the translation result is obtained and saved into a file.
def get_result(id, key):
    _params = {
        "auth_key" : my_key,
        "document_key" : key
    }
    response = requests.get(url_result.format(id),params=_params,allow_redirects=True)
    file_name = os.path.splitext(sys.argv[1])[0]
    with open(file_name + "_translated.txt", "wb") as file:
        file.write(response.content)
    print("Result written in " + file_name + "_translated.txt")

if len(sys.argv) == 1:
    print("No file provided! Please, provide the path of the file to be translated.") 
elif not os.path.exists(sys.argv[1]):
    print("Incorrect file! Please, provide a valid path for the file to be translated.") 
else:
    #The file passed as argument is translated and saved into a new file
    translate(sys.argv[1])    