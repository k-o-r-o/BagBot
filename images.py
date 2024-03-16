import requests
from bs4 import BeautifulSoup

def fetch_images():
    url = 'https://pixeljoint.com/pixels/new_icons.asp?ob=date'
    site = "https://pixeljoint.com"
    response = requests.get(url)
    text = response.text
    data = BeautifulSoup(text, 'html.parser')

    # Find all anchor elements with class "imglink"
    img_links = data.find_all('a', class_='imglink')

    total_urls = []  # Initialize the list to store all total_urls

    # Iterate over each anchor element and extract the href attribute
    for img_link in img_links:
        href = img_link['href']
        if '/pixelart/' in href:
            full_art_url = site + href

            # Append scheme if missing
            if not full_art_url.startswith("http"):
                full_art_url = "https://" + full_art_url

            # Fetch the HTML content of FullArt URL
            response_fullart = requests.get(full_art_url)
            text_fullart = response_fullart.text
            data_fullart = BeautifulSoup(text_fullart, 'html.parser')

            # Find the img tag with id 'mainimg'
            img_main = data_fullart.find('img', id='mainimg')
            if img_main:
                src_link = img_main['src']
                total_url = (site+src_link)
                total_urls.append(total_url)  # Append the total_url to the list

    return total_urls  # Return the list of total_urls

