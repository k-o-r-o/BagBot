from images import fetch_images

total_urls = fetch_images()
for url in total_urls:
    print(url)
