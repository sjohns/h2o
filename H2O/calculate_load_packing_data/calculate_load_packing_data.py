#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Stephen Johns

This script reads data from a CSV file and performs various data transformations, 
saving the results in CSV, Javascript, and JSON formats.

The input file name can be changed as well as the output file names except 
for the output_js_file_name since it is used as an input into the web form.

The output CSV file is only so the outputs can be reviewed

The output JS file must be copied to the root of the HTML directory

Timestamped files of the input file and all the outputs are created for backups.

Description and Explanation:
This script performs a series of data processing tasks:
1. Reads data from an input CSV file.
2. Cleans and transforms the data by removing NaN values, trimming spaces, and dropping/renaming specific columns.
3. Saves the cleaned data to a new CSV file with a timestamp for versioning.
4. Organizes the data into a nested dictionary structure suitable for JSON and JavaScript output.
5. Writes the structured data to JSON and JavaScript files, with timestamped backups for each.

The script is designed to be flexible, allowing the input and output file names to be easily changed. The inclusion of timestamped backups ensures that all versions of the data are preserved for future reference or rollback if necessary.
"""


import json
import datetime
from collections import defaultdict

# import pandas as pd
# import numpy as np
import duckdb

from typing import Optional, List

# Define file names for input and output
input_file_name = 'H2O New PRICE LIST & LOADING CHART 2024.csv'
output_js_file_name = 'load_packing_data.js'


def clean_string(s: str) -> str:
    """
    Clean and transform a string by removing leading/trailing spaces and double spaces.
    """
    if isinstance(s, str):
        # Remove leading and trailing spaces and replace double spaces with single spaces
        cleaned_s = ' '.join(s.strip().split())
        return cleaned_s
    else:
        return s


def drop_column_if_exists(df, column_name):
    if column_name in df.columns:
        df = df.drop(columns=[column_name])
    return df


# Get the current timestamp
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

df = duckdb.read_csv(input_file_name).df()

# Remove rows and columns that are all NaN (blank)
df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)

df.dropna(subset=['popularityScore'], inplace=True)

# Apply the clean_string function to all columns
df = df.map(clean_string)

df.reset_index(inplace=True,drop=True)

df.reset_index(inplace=True)

df['index'] = df['index'] + 1

df = df.rename(columns={'index': 'displayOrder'})

df['size'] = df['SKU'].str.split('"').str[0] + '"'

df['SKU'] = df['SKU'] + ' - ' + df['column3']

df = df.drop('column3', axis=1)


#
#########################################################
#
# Product Type
#
#########################################################
#
#

query = """
select 
    distinct
        productType
from
    df
order by 
    displayOrder
"""

df_productType = duckdb.sql(query).df()

df_productType.reset_index(inplace=True)

df_productType['index'] = df_productType['index'] + 1

df_productType = df_productType.rename(columns={'index': 'productTypeId'})

df_productType['productTypeId'] = 'productTypeId_' + df_productType['productTypeId'].astype(str)

query = """
select
    df_producttype.productTypeId as productTypeId,
    df.*
from
    df_productType,
    df
where
    df_productType.productType = df.productType
"""

df_with_product_id = duckdb.sql(query).df()


#
#########################################################
#
# SKU
#
#########################################################
#
#

query = """
select 
    distinct
        productTypeId,
        SKU
from
    df_with_product_id
order by
     displayOrder

"""

df_sku = duckdb.sql(query).df()

df_sku.reset_index(inplace=True)

df_sku['index'] = df_sku['index'] + 1

df_sku = df_sku.rename(columns={'index': 'skuId'})

df_sku['skuId'] = 'skuId_' + df_sku['skuId'].astype(str)

query = """
select
    df_sku.skuId as skuId,
    df_with_product_id.*
from
    df_sku,
    df_with_product_id
where
    df_sku.sku = df_with_product_id.sku
    and
    df_sku.productTypeId = df_with_product_id.productTypeId
"""

df_with_sku_id = duckdb.sql(query).df()

columns_to_convert_to_integer = ['displayOrder', 'popularityScore', 'eagleSticksPerTruckload','calculatedSticksPerBundle']  # List of columns to convert
df_with_sku_id[columns_to_convert_to_integer] = df_with_sku_id[columns_to_convert_to_integer].astype(int)

# Initialize a defaultdict to store the packing data
packing_data = {
    "date": str(timestamp),
    "productTypes": []
}

# Initialize a defaultdict to store product types
productTypes_dict = defaultdict(dict)

# Iterate over each row in the DataFrame
for _, row in df_with_sku_id.iterrows():
    productTypeId = row['productTypeId']
    if productTypeId not in productTypes_dict:
        productType_info = {
            'productTypeId': productTypeId,
            'productType': row['productType'],
            'skus': {}
        }
        productTypes_dict[productTypeId] = productType_info

    skuId = row['skuId']
    sku_info = row.to_dict()
    productTypes_dict[productTypeId]['skus'][skuId] = sku_info

    # Convert the product types dictionary to a list and assign to packing data
    packing_data["productTypes"] = list(productTypes_dict.values())

    # Convert the packing data to JSON
    json_data = json.dumps(packing_data, indent=4)

    # Create JavaScript code from the JSON data
    js_code = f"const packingData = {json_data};"

    # Write the JavaScript code to a .js file
    with open(output_js_file_name, 'w') as js_file:
        js_file.write(js_code)
