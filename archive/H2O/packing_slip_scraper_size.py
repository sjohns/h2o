# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 17:12:11 2024

Overview:
This script automates the process of selecting specific sizes from a webpage,
submitting an order, scraping the resulting packing slip data, and saving the
data into an HTML file. The script then opens the HTML file in Firefox for review.

Steps:
1. Initialize the Firefox WebDriver.
2. Open the target website.
3. Loop through predefined size ID arrays, select checkboxes, and submit orders.
4. Scrape packing slip data from the resulting webpage.
5. Save the scraped data into an HTML file.
6. Use Selenium to open the newly created HTML file in Firefox.

Dependencies:
- selenium
- os
- webbrowser
- time

@author:
Stephen
"""

import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Define the array of size IDs (manually created)
# Each sub-array should have between 2 and 5 size IDs
size_ids_array = [
    ['sizeId_9', 'sizeId_12'],  
    ['sizeId_9', 'sizeId_12','sizeId_6'], 
    ['sizeId_9', 'sizeId_12','sizeId_6','sizeId_7','sizeId_2'],
    ['sizeId_10', 'sizeId_5'],
    ['sizeId_10', 'sizeId_5','sizeId_17'], 
    ['sizeId_10', 'sizeId_5','sizeId_17','sizeId_19','sizeId_31'],
    ['sizeId_10', 'sizeId_9'],
    ['sizeId_9', 'sizeId_12','sizeId_6','sizeId_10','sizeId_17'],
    ['sizeId_36', 'sizeId_28'],
    ['sizeId_16', 'sizeId_28','sizeId_26','sizeId_29','sizeId_27'],
    ['sizeId_9', 'sizeId_36'],
    ['sizeId10', 'sizeId_26'],
    ['sizeId_9', 'sizeId_10','sizeId_16','sizeId_29','sizeId_27'],
    ['sizeId_12', 'sizeId_5','sizeId_17','sizeId_2','sizeId_27'],

]

# Initialize the Firefox driver
driver = webdriver.Firefox()

# Function to scrape packing slip data for a set of size IDs
def scrape_packing_slip(size_ids):
    """
    Scrapes packing slip data for a given set of size IDs.

    Parameters:
    size_ids (list): List of size IDs to be selected and processed.

    Returns:
    str: HTML content of the packing slip table.
    """
    for size_id in size_ids:
        try:
            print(f"Looking for checkbox parent td with size_id: {size_id}")
            # Locate the parent <td> containing the checkbox with the specified value
            parent_td = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[input[@name='selectedSize' and @value='{size_id}']]"))
            )
            
            print(f"Ensuring parent td {size_id} is interactable")
            # Ensure that the parent <td> is interactable
            parent_td = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//td[input[@name='selectedSize' and @value='{size_id}']]"))
            )
            
            # Click on the parent <td> to select the checkbox
            parent_td.click()
            print(f"Clicked parent td {size_id}")
        except Exception as e:
            print(f"Error with checkbox {size_id}: {e}")
            print("Current page source:")
            print(driver.page_source)
            continue

    try:
        print("Attempting to locate the 'Create Order' button.")
        # Click the "Create Order" button
        create_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create Order']"))
        )
        print("'Create Order' button found. Clicking it.")
        create_order_button.click()
    except Exception as e:
        print(f"Error locating or clicking the 'Create Order' button: {e}")
        return None

    try:
        print("Waiting for the packing slip details to be displayed.")
        # Wait for the packing slip details to be displayed
        time.sleep(3)  # Adjust the sleep time if necessary

        # Scrape the data from the packing slip table
        print("Attempting to locate the packing slip table.")
        packing_slip_table = driver.find_element(By.ID, 'orderTableDetail')
        packing_slip_html = packing_slip_table.get_attribute('outerHTML')
        print(f"Packing slip data: {packing_slip_html}")
        return packing_slip_html
    except Exception as e:
        print(f"Error scraping packing slip data: {e}")
        return None

# Open the target website
print("Opening the target website.")
driver.get('http://pipes/index1.html')  # Replace with the actual path to your HTML file

# List to store all packing slip data
all_packing_slip_data = []

# Loop through each set of size IDs in the array and scrape the packing slip data
for size_ids in size_ids_array:
    if 2 <= len(size_ids) <= 5:  # Ensure there are between 2 and 5 size IDs
        driver.refresh()
        time.sleep(2)  # Wait for the page to load
        packing_slip_data = scrape_packing_slip(size_ids)
        if packing_slip_data:
            all_packing_slip_data.append(packing_slip_data)

# Close the browser
print("Closing the browser.")
driver.quit()

# Function to update the packing_slips.html file
def update_html_file(packing_slip_data):
    """
    Updates the packing_slips.html file with new packing slip data.

    Parameters:
    packing_slip_data (list): List of HTML content strings for the packing slips.

    Returns:
    str: Absolute file path of the updated HTML file.
    """
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Packing Slips</title>
</head>
<body>
    <h3>Existing Packing Slips</h3>
    <!-- New packing slips will be appended here -->
    {}
</body>
</html>
    """

    # Combine the new packing slip data
    new_content = ''.join(packing_slip_data)

    # Read the existing HTML file and update it
    file_path = 'packing_slips.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_template.format(new_content))

    print(f"Packing slip content successfully written to {file_path}.")
    return os.path.abspath(file_path)

# Update the packing_slips.html file with the new data and get the file path
file_path = update_html_file(all_packing_slip_data)

# Use Selenium to open the new HTML file in Firefox
driver = webdriver.Firefox()
driver.get(f'file:///{file_path}')
