import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json

URL = "https://tutorial.math.lamar.edu/Classes/CalcII/TaylorSeries.aspx"


def fetching_page(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.3" #act like a browser
        },
        timeout=30
    )

    response.raise_for_status()

    return response.text


def parsing(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find(
        lambda tag:
        tag.name in ["main"]
    )

    if not title:
        raise ValueError("Main content not found in the HTML content.")

    items = []
    allowed_div_classes = { #these are the only div classses containing imp info
        "center-div",
        "example",
        "example-content",
        "soln-content",
    }

    for item in title.find_all_next():

        if item.name in ["h4", "p", "div", "mjx-container", "img"]:
            if item.name == "div":
                div_classes = set(item.get("class", []))
                if not div_classes & allowed_div_classes:
                    continue

            images = item.find_all("img") if item.name == "div" else [] #sadly div center-div class doesn't work :(
            text = item.get_text(" ", strip=True)

            if not text and item.name == "img":
                text = item.get("alt", "")

            if not text and not images:
                continue

            block_type = "unknown" #if there are any anomalies...

            if item.name == "h4":
                block_type = "heading"
            elif item.name == "p":
                block_type = "paragraph"
            elif item.name == "mjx-container":
                parent_p = item.find_parent("p")
                is_inside_p = parent_p is not None 
                if is_inside_p:
                    block_type = "inline-math"
                else:
                    block_type = "equation"
            elif item.name == "img":
                block_type = "image"
            elif item.name == "div":
                if "example" in item.get("class", []):
                    block_type = "example"
                elif "example-content" in item.get("class", []):
                    block_type = "example-content"
                elif "soln-content" in item.get("class", []):
                    block_type = "solution"
                elif "center-div" in item.get("class", []):
                    block_type = "image"
                else: 
                    block_type = "example" #apparently it doesn't recognize the example class for some reason, so we will just bruteforce it

            content = {
                "html_tag": item.name,
                "type": block_type,
                "text": text
            }

            if item.name == "img":
                content["src"] = item.get("src", "")
                content["alt"] = item.get("alt", "")
                content["class"] = item.get("class", [])
            elif images:
                content["images"] = [
                    {
                        "src": image.get("src", ""),
                        "alt": image.get("alt", ""),
                        "class": image.get("class", [])
                    }
                    for image in images
                ]

            items.append({
                **content
            })

    return items


def save_json(data, filename="categorical_analysis2.json"):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def fetching_rendered_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")
        html = page.content()

        browser.close()

    return html

if __name__ == "__main__":

    html = fetching_rendered_page(URL)

    items = parsing(html)   

    article = {
        "metadata": {
            "title": "Tangent Lines and Rates of Change",
            "url": URL
        },
        "content": items
    }

    save_json(article)

    print(f"Extracted {len(items)} content blocks.")