# random test file to test random functionality of code ... 

import requests 
from bs4 import BeautifulSoup

URL = "https://tutorial.math.lamar.edu/Classes/CalcI/Tangents_Rates.aspx"

def fetching_page(url):
    response = requests.get(
        url, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" # User-Agent header to mimic a browser request
        },
        timeout=30
    )
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def parsing(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting the title of the page
    title = soup.find(
        lambda tag: 
        tag.name in ['main'] 
    ) #verify that we got the title correctly

    if not title: 
        raise ValueError("Title not found in the HTML content.")

    items = []

    for item in title.find_all_next():
        
        if item.name in ['div']: 
            items.append(item['class'])

    return items


print(parsing(fetching_page(URL)))




    