# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:37:09 2024

@author: Stephen
"""

import pandas as pd
import math
import json
import datetime
from typing import Optional, List, Tuple
import os
from collections import defaultdict


# Get the current timestamp
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


# Specify the file name
input_file_name = 'mysql_packing_data.json'
output_json_file_name ='H2O Truck Load Packing Data MySQL JSON.json'
output_js_file_name ='load_packing_data_new.js'


def timestamp_file(input_file: str, timestamp: str) -> str:
    """
    Append the timestamp to the input file name and return the new file name.

    Args:
        input_file (str): The original file name.
        timestamp (str): The timestamp to append.

    Returns:
        str: The new file name with the timestamp.
    """
    # Extract the base name and file extension from the input file
    base_name, file_extension = os.path.splitext(input_file)

    # Create a new file name with the timestamp
    new_file_name = f"{base_name}_{timestamp}{file_extension}"

    return new_file_name


def calculate_lcm_of_bundles(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Calculate the LCM of bundle skus for the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing Product Id and calculated bundle sku data.

    Returns:
        Tuple[pd.DataFrame, int]: A DataFrame with added 'Bundle sku' column and the LCM value.
    """
    try:
        # Create a dictionary with 'Product_Id' as keys and 'Calculated Bundles per Truckload' as values
        bundles = {}
        for index, row in df.iterrows():
            bundleId = row['bundleId']
            calculatedBundlesPerTruckload = row['calculatedBundlesPerTruckload']
            bundles[bundleId] = calculatedBundlesPerTruckload

        # Convert the dictionary values to a set
        bundles_set = set(bundles.values())

        # Calculate the LCM of the values in the set
        lcm_result = math.lcm(*bundles_set)

        # Modify the dictionary by setting values to lcm_result / existing dictionary value (as a whole number)
        for bundleId, existing_value in bundles.items():
            gcd_value = math.gcd(lcm_result, existing_value)
            new_value = lcm_result // gcd_value

            # Check if the division result is a whole number (integer)
            if new_value != int(new_value):
                raise ValueError(f"Error: Division did not result in an integer for '{bundleId}'")

            bundles[bundleId] = int(new_value)

        # Add a new column to the DataFrame with values from the dictionary
        df['calculatedBundleSize'] = df['bundleId'].map(bundles)

        return df, lcm_result

    except FileNotFoundError:
        raise FileNotFoundError("File not found. Please provide the correct file path.")

    except KeyError:
        raise KeyError("The 'SKU' or 'Bundles Per Truckload' column does not exist in the Excel file.")

    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
        

def clean_string(s: str) -> str:
    """
    Clean and transform a string by removing leading/trailing spaces and double spaces.

    Args:
        s (str): The input string.

    Returns:
        str: The cleaned string.
    """
    if isinstance(s, str):
        # Remove leading and trailing spaces and replace double spaces with single spaces
        cleaned_s = ' '.join(s.strip().split())
        return cleaned_s
    else:
        return s
    
    
def read_and_process_JSON(input_file_name: str) -> Optional[pd.DataFrame]:
    """

    Reads a JSON file

    Args:
        input_file_name (str): The path to the JSON file.

    Returns:
        Optional[pd.DataFrame]: The DataFrame containing the selected data, or None if an error occurs.

    """
    

    # Read the JSON into a DataFrame
    df_temp = pd.read_json(input_file_name)
    archive_file_name = timestamp_file(input_file_name,timestamp)
    df_temp.to_csv(archive_file_name, index=False)
    # Remove rows and columns that are all NaN (blank)
    df_temp = df_temp.dropna(how='all', axis=0).dropna(how='all', axis=1)
    # Apply the clean_string function to all columns
    df_temp = df_temp.map(clean_string)
#    df_temp['calculatedBundlesPerTruckload'] = round(100 /df_temp['bundleLoadPercentage'],0)
#    df_temp['calculatedBundlesPcsPerTruckload'] = df_temp['bundlePcsLift'] * df['calculatedBundlesPerTruckload']

    # List of column names to convert to integers
    columns_to_convert = [ 
        
        'productTypeId',
        'skuId',
        'skuLength',
        'skuFtLoad',
        'bundleId',
        'bundlePcsLift',
        'bundleFtLift',
        'bundleFtLoad',
        'calculatedBundlesPerTruckload',
        'calculatedBundlePcsPerTruckload',
        ]
    
    for col in columns_to_convert:

        if col in df_temp.columns:

            df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce').fillna(0).astype(int)
 
    df_temp['calculatedBundlesPerTruckload'] = round(100 /df_temp['bundleLoadPercentage'],0)


    for col in columns_to_convert:

        if col in df_temp.columns:

            df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce').fillna(0).astype(int)

    df_temp['calculatedBundlesPcsPerTruckload'] = df_temp['bundlePcsLift'] * df_temp['calculatedBundlesPerTruckload']




    
    return df_temp

try:
    # Call the read_and_process_csv function
    df = read_and_process_JSON(input_file_name)
    if df is None:
        exit(1)  # Exit if DataFrame is not created
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

# df['calculatedBundlesPerTruckload'] = round(100 /df['bundleLoadPercentage'],0)
# #df['bundlesPerTruckload'] =  df['calculatedBundlesPerTruckload']
# df['calculatedBundlePcsPerTruckload'] = df['bundlePcsLift'] * df['calculatedBundlesPerTruckload']


    
# Calculate LCM and bundle sizes

df, lcm = calculate_lcm_of_bundles(df)

archive_file_name = timestamp_file(output_json_file_name,timestamp)
df.to_json(archive_file_name, index=False)


# Initialize a defaultdict to store the packing data
packing_data = {
    "date": str(timestamp),
    "lcm": lcm,
    "productTypes": []
}

# Initialize a defaultdict to store product types
productTypes_dict = defaultdict(list)


# Iterate over each row in the DataFrame
for _, row in df.iterrows():
    # Extract data from the row
    productTypeId = row['productTypeId']
    productType = row['productType']
    
    # Create a dictionary for the current SKU
    skuId = row['skuId']
    skuSize = row['skuSize']
    skuPopularity = row['skuPopularity']
    sku_info = {
        'skuId': skuId,
        'skuSize': skuSize,
        'skuPopularity': skuPopularity,
        'bundles' : {},
        'productTypeId': productTypeId,
    }
    
    # Create a dictionary for the current bundle
    bundleId = row['bundleId']
    bundleSize = row['bundleSize']
    bundlePcsLift = row['bundlePcsLift']
    bundleFtLift = row['bundleFtLift']
    bundleLiftsLoad = row['bundleLiftsLoad']           
    bundleLoadPercentage = row['bundleLoadPercentage']
    calculatedBundlesPerTruckload = row['calculatedBundlesPcsPerTruckload']
    calculatedBundlesPcsPerTruckload = row['calculatedBundlesPcsPerTruckload']           
    calculatedBundleSize = row['calculatedBundleSize']    
        
    bundle_info = {
        'bundleId': bundleId,
        'sticksPebundleSizerBundle': bundleSize,
        'bundlePcsLift' : bundlePcsLift,
        'bundleFtLift' : bundleFtLift,
        'bundleLiftsLoad' : bundleLiftsLoad,
        'bundleLoadPercentage' :  bundleLoadPercentage,       
        'calculatedBundlesPcsPerTruckload' : calculatedBundlesPcsPerTruckload,
        'calculatedBundlesPcsPerTruckload' : calculatedBundlesPcsPerTruckload,
        'calculatedBundleSize' :  calculatedBundleSize,
        'productTypeId': productTypeId,
        'skuId': skuId,
    }
    
    # Check if the product type exists in the dictionary
    if productTypeId not in productTypes_dict:
        # If product type doesn't exist, add it to the dictionary
        productType_info = {
            'productTypeId': productTypeId,
            'productType': productType,
            'skus': {}  # Initialize empty dictionary for skss
        }
    productTypes_dict[productTypeId] = productType_info
    
    
    # Check if the sku exists in the product type dictionary
    if skuId not in productTypes_dict[productTypeId]['skus']:
        # If sku doesn't exist, add it to the dictionary
        productTypes_dict[productTypeId]['skus'][skuId] = sku_info
            
    
    # Add bundle info to the sku dictionary if it doesn't already exist
    if bundleId not in productTypes_dict[productTypeId]['skus'][skuId]['bundles']:
        productTypes_dict[productTypeId]['skus'][skuId]['bundles'][bundleId] = bundle_info



# # Convert defaultdict to regular dictionary
productTypes_dict = dict(productTypes_dict)
    
packing_data["productTypes"] = productTypes_dict


# Save the JSON data to a file
with open(output_json_file_name, 'w') as json_file:
    json.dump(packing_data, json_file, indent=4)

archive_file_name = timestamp_file(output_json_file_name,timestamp)

# Save the JSON data to a file
with open(archive_file_name, 'w') as json_file:
    json.dump(packing_data, json_file, indent=4)

# Convert the Python dictionary to a JavaScript object
js_code = f"const packingData = {json.dumps(packing_data, indent=4)};"

productTypes_dict = dict(productTypes_dict)
    
packing_data["productTypes"] = productTypes_dict

# Save the JSON data to a file
with open(output_json_file_name, 'w') as json_file:
    json.dump(packing_data, json_file, indent=4)

archive_file_name = timestamp_file(output_json_file_name,timestamp)

# Save the JSON data to a file
with open(archive_file_name, 'w') as json_file:
    json.dump(packing_data, json_file, indent=4)

# Convert the Python dictionary to a JavaScript object
js_code = f"const packingData = {json.dumps(packing_data, indent=4)};"


# Write the JavaScript code to a .js file
with open(output_js_file_name, 'w') as js_file:
    js_file.write(js_code)

archive_js_file_name = timestamp_file(output_js_file_name,timestamp)

# Write the JavaScript code to a .js file
with open(archive_js_file_name, 'w') as js_file:
    js_file.write(js_code)

















