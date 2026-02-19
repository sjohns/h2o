#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:38:46 2023

@author: stephen

This script reads initial data from an CSV file, processes it, and writes it to a new initial CSV file.

"""

# File paths
input_file_name = 'H2O_new_initial_data.csv'
output_filename = 'H2O_new_initial_data_processed.csv'

import pandas as pd
import duckdb

from typing import Optional, List

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
    
def drop_columns_if_exist(df, columns):
    existing_columns = [col for col in columns if col in df.columns]
    if existing_columns:
        df.drop(columns=existing_columns, inplace=True)



df = duckdb.read_csv(input_file_name).df()

df = df.rename(columns={'sizeActive': 'skuActive'})
df = df.rename(columns={'sizePopularityScore': 'skuPopularityScore'})
df = df.rename(columns={'sticksPerTruckload': 'eagleSticksPerTruckload'})
df = df.rename(columns={'sticksPerBundle': 'eagleSticksPerBundle'})
df = df.rename(columns={'bundlesPerTruckload': 'originalBundlesPerTruckload'})

# Columns to drop
columns_to_drop = ['column02', 'productTypeDisplayOrder',]

# Drop the columns if they exist
drop_columns_if_exist(df, columns_to_drop)





# Remove rows and columns that are all NaN (blank)
df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
# Apply the clean_string function to all columns
df = df.map(clean_string)

df.dropna(subset=['skuPopularityScore'], inplace=True)

df.reset_index(inplace=True)

df['index'] = df['index'] + 1

df = df.rename(columns={'index': 'bundleId'})



df['bundleDescription'] = df['size']

df['productType'] = df['productType'].str.split('"').str[1]


df['size'] = df['size'].str.split('"').str[0] + '"'

df = df.map(clean_string)

df['sku'] = df['size'] + ' ' + df['productType']

query = """
select 
    distinct
        productType
from
    df
order by productType
"""

df_productType = duckdb.sql(query).df()

df_productType.reset_index(inplace=True)

df_productType['index'] = df_productType['index'] + 1

df_productType = df_productType.rename(columns={'index': 'productTypeId'})

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

query = """
select 
    distinct
        productTypeId,
        size
from
    df_with_product_id
order by productTypeId
"""

df_size = duckdb.sql(query).df()

df_size.reset_index(inplace=True)

df_size['index'] = df_size['index'] + 1

df_size = df_size.rename(columns={'index': 'skuId'})

query = """
select
    df_size.skuId as skuId,
    df_with_product_id.*
from
    df_size,
    df_with_product_id
where
    df_size.size = df_with_product_id.size
    and
    df_size.productTypeId = df_with_product_id.productTypeId
"""

df_with_sku_id = duckdb.sql(query).df()






df_with_sku_id['bundleId'] = 'bundleId_' + df_with_sku_id['bundleId'].astype(str)
#df_with_siku_id['SKUId'] = 'SKUId_' + df_with_siku_id['skuId'].astype(str)
df_with_sku_id['skuId'] = 'skuId_' + df_with_sku_id['skuId'].astype(str)
df_with_sku_id['productTypeId'] = 'productTypeId_' + df_with_sku_id['productTypeId'].astype(str)

query = """
select
    *
from
    df_with_sku_id
order by productTypeId, skuId, bundleId
"""

df_rows_ordered = duckdb.sql(query).df()





# Reorder columns by location (index)

# column_order = [1, 3, 4, 5, 6, 0, 7, 8, 9, 2, 10, 11, 12, 13, 14]  # Specify the desired column locations
# # # Specify the desired column locations

# df_columns_ordered = df_with_size_id[df_with_size_id.columns[column_order]]

# Write the DataFrame to a CSV file

# query = """
# select
#     *
# from
#     df_columns_ordered
# order by
#     productTypeDisplayOrder,
#     productType,
#     size
# """

# df_rows_ordered = duckdb.sql(query).df()

# df_rows_ordered = df_with_size_id

# df_rows_ordered['calculated_bundles_per_truckload'] = round(100 /df_rows_ordered['Eagle-%_LOAD_Per_Lift'],0)
# df_rows_ordered['bundlesPerTruckload'] =  df_rows_ordered['calculated_bundles_per_truckload']
# df_rows_ordered['sticksPerTruckload'] = df_rows_ordered['sticksPerBundle'] * df_rows_ordered['bundlesPerTruckload']


# # Update the bundlesPerTruckload and sticksPerTruckload based on the condition
# condition = df_rows_ordered['calculated_bundles_per_truckload'] != df_rows_ordered['bundlesPerTruckload']

# # Set bundlesPerTruckload to calculated_bundles_per_truckload where the condition is True
# df_rows_ordered.loc[condition, 'bundlesPerTruckload'] = df_rows_ordered.loc[condition, 'calculated_bundles_per_truckload']

# # Update sticksPerTruckload to sticksPerBundle * calculated_bundles_per_truckload where the condition is True
# df_rows_ordered.loc[condition, 'sticksPerTruckload'] = df_rows_ordered.loc[condition, 'sticksPerBundle'] * df_rows_ordered.loc[condition, 'calculated_bundles_per_truckload']





df_rows_ordered.to_csv(output_filename, index=False)  # Set index=False to exclude the row index

