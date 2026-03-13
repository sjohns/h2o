# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 17:12:11 2024

Overview:
This script automates the process of selecting specific SKU IDs from a webpage,
submitting an order, scraping the resulting packing slip data, and saving the
data into an HTML file. The script then creates a ZIP archive of the HTML file
and generates timestamped copies of both the HTML and ZIP files. Finally, it
opens the original HTML file in Firefox for review.

Steps:
1. Initialize the Firefox WebDriver.
2. Open the target website (a local HTML file).
3. Loop through predefined SKU ID arrays, select checkboxes, and submit orders.
4. Scrape packing slip data from the resulting webpage.
5. Save the scraped data into an HTML file.
6. Create a ZIP archive of the HTML file.
7. Generate timestamped copies of both the HTML and ZIP files.
8. Use Selenium to open the original HTML file in Firefox.

Dependencies:
- selenium: For automating web interactions.
- os: For handling file paths and operations.
- time: For fixed wait periods between actions.
- pathlib: For handling file paths in an object-oriented way.
- datetime: For generating timestamps.
- shutil: For copying files.
- zipfile: For creating ZIP archives.

@author:
Stephen
"""

import os
import shutil  # Used for copying files
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By  # Allows locating elements by their attributes (e.g., ID, XPath)
from selenium.webdriver.support.ui import WebDriverWait  # Waits for elements to meet conditions
from selenium.webdriver.support import expected_conditions as EC  # Defines the conditions to wait for
from pathlib import Path  # Provides an object-oriented approach to file paths
import time  # Used for fixed sleep intervals

# Default to this repository's html directory.
# Optional override: H2O_HTML_DIR=/path/to/html
base_directory = Path(
    os.environ.get('H2O_HTML_DIR', Path(__file__).resolve().parent / 'html')
)

# Define the path to the index.html file
index_file = base_directory / 'index.html'

# Convert the file path to a URL that can be opened in a browser
url = index_file.resolve().as_uri()

# Initialize the Firefox WebDriver
driver = webdriver.Firefox()

# Define an array of SKU ID arrays for the automation process
# Each sub-array contains between 1 and 5 SKU IDs to be selected on the webpage
sku_ids_array = [
     ['skuId_68', 'skuId_69', 'skuId_70', 'skuId_71', 'skuId_72'],
    ['skuId_32', 'skuId_33', 'skuId_52', 'skuId_53', 'skuId_54'],
     ['skuId_50', 'skuId_55', 'skuId_63'],
      ['skuId_2', 'skuId_3'],
    # ['skuId_18'], 
    # ['skuId_19'], ['skuId_44'],
    # ['skuId_9', 'skuId_12'],
    # ['skuId_9', 'skuId_12', 'skuId_6'],
    # ['skuId_9', 'skuId_12', 'skuId_6', 'skuId_7', 'skuId_2'],
    # ['skuId_10', 'skuId_5'],
    # ['skuId_10', 'skuId_5', 'skuId_17'],
    # ['skuId_10', 'skuId_5', 'skuId_17', 'skuId_19', 'skuId_31'],
    # ['skuId_10', 'skuId_9'],
    # ['skuId_9', 'skuId_12', 'skuId_6', 'skuId_10', 'skuId_17'],
    # ['skuId_36', 'skuId_28'],
    # ['skuId_9', 'skuId_36'],
    # ['skuId_10', 'skuId_26'],
    # ['skuId_9', 'skuId_10', 'skuId_16', 'skuId_29', 'skuId_27'],
    # ['skuId_12', 'skuId_5', 'skuId_17', 'skuId_2', 'skuId_27'],
]

# Function to scrape packing slip data for a set of SKU IDs
def scrape_packing_slip(sku_ids):
    """
    Scrapes packing slip data for a given set of SKU IDs by selecting the corresponding
    checkboxes on the webpage and submitting the form.

    Parameters:
    sku_ids (list): List of SKU IDs to be selected and processed.

    Returns:
    str: HTML content of the packing slip table if successful, or None if an error occurs.
    """
    for sku_id in sku_ids:
        try:
            # Locate the <td> element containing the checkbox with the specified SKU ID
            parent_td = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[input[@name='selectedsku' and @value='{sku_id}']]"))
            )
            
            # Ensure that the parent <td> is interactable (clickable)
            parent_td = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//td[input[@name='selectedsku' and @value='{sku_id}']]"))
            )
            
            # Click on the <td> to select the checkbox
            parent_td.click()
            print(f"Clicked checkbox for SKU ID: {sku_id}")
        except Exception as e:
            print(f"Error with checkbox {sku_id}: {e}")
            print("Current page source:")
            print(driver.page_source)  # Useful for debugging
            continue  # Skip to the next SKU ID if there's an error

    try:
        # Locate and click the "Create Order" button
        create_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create Order']"))
        )
        create_order_button.click()
        print("Clicked 'Create Order' button.")
    except Exception as e:
        print(f"Error locating or clicking the 'Create Order' button: {e}")
        return None

    try:
        # Wait for the packing slip details to be displayed
        time.sleep(3)  # Fixed wait to ensure the details are loaded

        # Locate the packing slip table by its ID and extract its HTML content
        packing_slip_table = driver.find_element(By.ID, 'orderTableDetail')
        packing_slip_html = packing_slip_table.get_attribute('outerHTML')
        print(f"Scraped packing slip data: {packing_slip_html}")
        return packing_slip_html
    except Exception as e:
        print(f"Error scraping packing slip data: {e}")
        return None

# Open the target website (local HTML file)
print("Opening the target website.")
driver.get(url)

# List to store all the scraped packing slip data
all_packing_slip_data = []

# Loop through each set of SKU IDs and scrape the corresponding packing slip data
for sku_ids in sku_ids_array:
    if 1 <= len(sku_ids) <= 5:  # Ensure there are between 1 and 5 SKU IDs
        driver.refresh()  # Refresh the page before each new selection

        # Wait for the page to load
        time.sleep(2)  # Fixed wait time for page load
        
        packing_slip_data = scrape_packing_slip(sku_ids)
        if packing_slip_data:
            all_packing_slip_data.append(packing_slip_data)

# Close the browser after all data has been scraped
print("Closing the browser.")
driver.quit()

# Function to update the packing_slips.html file with the scraped data, create ZIP files, and timestamped copies
def update_html_file(packing_slip_data):
    """
    Updates the packing_slips.html file with new packing slip data, creates a ZIP archive,
    then creates timestamped copies of both the HTML and ZIP files.

    Parameters:
    packing_slip_data (list): List of HTML content strings for the packing slips.

    Returns:
    str: Absolute file path of the updated HTML file.
    """
    # HTML template with a placeholder for the packing slip content
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Packing Slips</title>
    <style>
         /* Packing slip table styling */
         table {{
             width: 100%;
             border-collapse: collapse;
         }}

         th, td {{
             border: 1px solid black;
             padding: 5px;
         }}

         th {{
             text-align: center;
         }}

         td {{
             text-align: right;
         }}

         td.left {{
             text-align: left;
         }}

         tr:nth-child(even) {{
             background-color: #f2f2f2;
         }}

         tr:hover {{
             background-color: #ddd;
         }}
     </style>
</head>
<body>
    <h3>Existing Packing Slips</h3>
    <!-- New packing slips will be appended here -->
    {content}
</body>
</html>
    """

    new_content = ''.join(packing_slip_data)

    # Step 1: Create the main HTML file
    file_path = 'packing_slips.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_template.format(content=new_content))
    print(f"Packing slip content successfully written to {file_path}.")

    # Step 2: Create ZIP archive for the main HTML file
    zip_file_path = 'packing_slips.zip'
    with ZipFile(zip_file_path, 'w', ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))
    print(f"Created ZIP archive: {zip_file_path}")

    # Step 3: Create a timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamped_file_path = f'packing_slips_{timestamp}.html'
    timestamped_zip_path = f'packing_slips_{timestamp}.zip'

    # Step 4: Copy the original HTML file to the timestamped version
    shutil.copy(file_path, timestamped_file_path)
    print(f"Copied HTML file to {timestamped_file_path}.")

    # Step 5: Copy the original ZIP file to the timestamped version
    shutil.copy(zip_file_path, timestamped_zip_path)
    print(f"Copied ZIP file to {timestamped_zip_path}.")

    return os.path.abspath(file_path)

# Update the packing_slips.html file with the new data and get the file path
file_path = update_html_file(all_packing_slip_data)

# Use Selenium to open the newly created HTML file in Firefox
driver = webdriver.Firefox()
driver.get(f'file:///{file_path}')
