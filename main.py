import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the webdriver (using Firefox in this case)
driver = webdriver.Firefox()

# Target URL
url = "https://www.divan.ru/category/divany"

# Open the webpage
driver.get(url)

# Allow some time for the page to load completely
time.sleep(5)

# Use WebDriverWait to ensure that product elements are loaded
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[@itemprop='name']"))
    )

    # Find all product names using XPath
    product_names = driver.find_elements(By.XPATH,
                                         "//span[@itemprop='name'] | //h1[@class='PJZwc' and @itemprop='name']")

    # Find all prices using XPath
    product_prices = driver.find_elements(By.XPATH, "//span[@class='ui-LD-ZU KIkOH' and @data-testid='price']")

    # Ensure the number of product names matches the number of prices
    if len(product_names) != len(product_prices):
        print("Mismatch between number of product names and prices.")

    # List to store parsed data
    parsed_data = []

    # Iterate through each product and extract the information
    for i in range(min(len(product_names), len(product_prices))):
        try:
            # Get the product name
            title = product_names[i].text

            # Get the price and strip out the currency part (e.g., "руб.")
            price = product_prices[i].text.replace("руб.", "").strip()

            # You can also add link or any other data if needed
            parsed_data.append([title, price])
        except Exception as e:
            print(f"An error occurred while parsing a product: {e}")
            continue

except Exception as e:
    print(f"An error occurred while waiting for product elements: {e}")

# Close the browser
driver.quit()

# Ensure parsed_data is defined even if no products are found
if 'parsed_data' not in locals():
    parsed_data = []

# Save the data into a CSV file
with open("divan_products.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Product Name', 'Price'])
    # Write the product rows
    writer.writerows(parsed_data)

print("Data saved to divan_products.csv")
