import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=laptop&page={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

products = []

for page in range(1, 41):
    url = base_url.format(page)
    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    product_divs = soup.find_all(
        "div", {"data-component-type": "s-search-result"})

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
