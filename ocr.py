# import the necessary packages
import cv2
import urllib.request
import numpy as np
import json
import re
import pytesseract
from PIL import Image
from flask import Flask,request,jsonify
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
run_with_ngrok(app)  

def word_to_number_converter(word):
        word_dict = {
            "L" : "1",
            "l" : "1",
            "b" : "6",
            "O" : "0",
            "A" : "4",
            "Z" : "2",
            "z" : "2",
            "S" : "5",
            "s" : "5",
            "B" : "8",
            "D" : "0",
            "o" : "0",
            "?" : "7",
            "e" : ""
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res

@app.route('/')
def home():
    # return json.loads(request.data)
    data = json.loads(request.data)
    print(data)
    req = urllib.request.urlopen(data['url'])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshed = cv2.threshold(cv2.medianBlur(gray, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    raw_extracted_text = pytesseract.image_to_string((threshed))
    result = re.findall('\w{16}', raw_extracted_text.replace(" ", ""))
    if len(result) != 0:
        hasil = {
                'result': word_to_number_converter(result[0].replace(" ", "")),
                'raw': raw_extracted_text
            }
    else:
        hasil = {
                'result': "FOTO KTP TIDAK DIKENALI",
                'raw': raw_extracted_text
            }
    return hasil
    #return raw_extracted_text
app.run()
