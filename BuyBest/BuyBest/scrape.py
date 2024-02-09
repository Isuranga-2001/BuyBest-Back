import requests
from bs4 import BeautifulSoup
import mimetypes

url = 'https://www.laptop.lk/index.php/product-category/'  # Replace with the target website URL
arr = []

f = open("urls.txt", "a")


def get_body_content(base):
    try:
        response = requests.get(base)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.body.text
        return body_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def is_html(base):
    try:
        response = requests.get(base)
        content_type = response.headers['Content-Type']
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def findAllUrls(base):
    reqs = requests.get(base)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    ln = len(base) - 1

    for link in soup.find_all('a'):
        sublink = link.get('href')
        try:
            if sublink[0:ln + 1] == base:
                if is_html(base):
                    f.append(sublink + '\n')
                    if sublink not in arr:
                        arr.append(sublink)
                else:
                    findAllUrls(sublink)
        except:
            continue


findAllUrls(url)
f.close()