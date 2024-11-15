# from bs4 import BeautifulSoup
# import requests
# import pandas as pd

# relDigital = requests.get('https://www.jumia.co.ke/all-products/')

# name_info = []
# price_info = []
# rating_info = []


# for page in range(1, 51):
#     url = "https://www.jumia.co.ke/all-products/" + \
#         "?page=" + str(page) + "#catalog-listing"
#     furl = requests.get(url)
#     jsoup = BeautifulSoup(furl.content, 'html.parser')
#     products = jsoup.find_all('div', class_='info')

#     for product in products:
#         name = product.find('h3', class_='name').text.replace('\n', '')
#         price = product.find('div', class_='prc').text.replace('\n', '')

#         try:
#             rating = product.find(
#                 'div', class_='stars_s').text.replace('\n', '')
#         except:
#             rating = 'None'

#         name_info.append(name)
#         price_info.append(price)
#         rating_info.append(rating)

#         print(name_info, price_info, rating_info)


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=laptop&page={}"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# empty list to store product data
products = []

# Scrapping of first 40 pages
for page in range(1, 41):
    url = base_url.format(page)
    print(f"Scraping page {page}...")

    # Get the page content
    response = requests.get(url, headers=headers)

    # If the response status is not 200 (OK), skip the page
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product containers
    product_divs = soup.find_all(
        "div", {"data-component-type": "s-search-result"})

    # Loop through each product container
    for product in product_divs:
        try:
            # Extract product name
            name = product.h2.a.text.strip()

            # Extract product price
            price = product.find("span", "a-price-whole")
            price = price.text.strip() if price else "N/A"

            # Extract product rating
            rating = product.find("span", class_="a-icon-alt")
            rating = rating.text.split()[0] if rating else "No rating"

            product_data = {
                "Product Name": name,
                "Price (INR)": price,
                "Rating": rating
            }

            products.append(product_data)

        except Exception as e:
            print(f"Error processing product: {e}")
            continue

    # Sleep to avoid getting blocked by Amazon
    time.sleep(1)

df = pd.DataFrame(products)

df.to_csv("amazon_products.csv", index=False)

print("Data scraping completed and saved to amazon_products.csv")
