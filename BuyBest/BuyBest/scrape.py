import requests
from bs4 import BeautifulSoup

url = 'https://www.laptop.lk/index.php/product-category/laptops-desktops/'
baseUrl = "https://www.laptop.lk/index.php/product/"
arr = []


def get_body_content(base):
    try:
        response = requests.get(base)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.body.text
        return body_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def findAllUrls(base):
    reqs = requests.get(base)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    arr = []
    ln = len(baseUrl) - 1

    f = open("urls.txt", "w")

    for link in soup.find_all('a'):
        sublink = link.get('href')
        try:
            if sublink[0:ln + 1] == baseUrl:
                f.writelines(sublink + '\n')
                if sublink not in arr:
                    arr.append(sublink)

        except:
            continue

    f.close()
    return arr




count = 5

# scan bu body tag
for i in arr:
    count -= 1
    if count == 0:
        break
    print(get_body_content(i).strip())
    print("\n")