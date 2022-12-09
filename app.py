from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import urlopen
import json

app = Flask(__name__)


@app.route('/')
#@app.route('/home')
def home():
    return render_template("results.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    isbn = output["ISBN"]

    #isbn = "9780321543257"
    # isbn = "1118290275"

    url = "https://openlibrary.org/isbn/"+isbn+".json"
    
    # store the response of URL
    response = urlopen(url)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())

    # formats the data_json to be readable
    data_json_str = json.dumps(data_json, indent=2)
    
    # print the json response
    # print(data_json_str)

    title = data_json["title"]

    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("TM", "")
    title = title.replace(" ", "-")
    title = title.lower()

    #print(title)

    valoreBooks = "https://www.valorebooks.com/textbooks/"+title+"/"+isbn

    from scraper_api import ScraperAPIClient
    client = ScraperAPIClient('95a43ead4493ef31bbf4704a4bfaf81a')
    result = client.get(url = valoreBooks).text
    #print(result)
    start_urls =[client.scrapyGet(url = 'http://httpbin.org/ip')]
    def parse(self, response):
        yield scrapy.Request(client.scrapyGet(url = 'http://httpbin.org/ip'), self.parse)

    soup = BeautifulSoup(result, 'lxml')

    first = soup.find_all('span', class_ = 'commaFormat')

    print(first)

    print(type(first))

    x = 1
    used = ""
    new = ""
    alternate = ""
    for points in first:
        if x == 1:
            new = str(points.text)
        elif x == 2:
            used = str(points.text)
        elif x == 3:
            alternate = str(points.text)
        x = x + 1

    print("The used book costs "+used)
    print("The new book costs "+new)
    print("The alternate book costs "+alternate)

    return render_template('results.html', used = used)
    

if __name__ == "__main__":
    app.run(debug=True)