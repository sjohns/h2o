# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:24:47 2024

@author: Stephen
"""

# # Update product_type where product_type is "AWWA C900 PVC 20'" and source is "jme_CIODLoadingChart"
# df.loc[(df['product_type'] == "AWWA C900 PVC 20'") & (df['source'] == "jme_CIODLoadingChart"), 'product_type'] = "DR18 PVC PIPE C-900 - GASKET"


# File paths
input_file_name = 'eagle_charts.json'
output_filename = 'eagle_charts_processed.csv'

import pandas as pd
import numpy as np
import duckdb


from typing import Optional, List

query_df = """
SELECT
    distinct product_type, source
FROM
    df
"""

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

df = duckdb.read_json(input_file_name).df()

# Apply the clean_string function to all columns
df = df.map(clean_string)

df_1 = duckdb.sql(query_df).df()

def duplicate_and_update(df, original_product_type, new_product_type1, new_product_type2):
    # Filter the rows that need to be duplicated
    rows_to_duplicate = df[df['product_type'] == original_product_type].copy()

    # Update the product_type of the new duplicated rows
    rows_to_duplicate['product_type'] = new_product_type1

    # Update the product_type of the original rows
    df.loc[df['product_type'] == original_product_type, 'product_type'] = new_product_type2

    # Concatenate the new rows with the original DataFrame
    df = pd.concat([df, rows_to_duplicate], ignore_index=True)
    
    return df

# Duplicate and update for "GRAVITY SEWER 14'"
df = duplicate_and_update(df, "GRAVITY SEWER 14'", "SDR35 PVC PIPE GRAVITY SEWER - GASKET", "SDR26 PVC PIPE GRAVITY SEWER - GASKET")

# Update product_type where product_type is "AWWA C900 PVC 20'" and source is "jme_CIODLoadingChart"
df.loc[(df['product_type'] == "AWWA C900 PVC 20'") & (df['source'] == "jme_CIODLoadingChart"), 'product_type'] = "PVC PIPE C-900 - GASKET"

# Rename product_type where it matches the specific value
df.loc[df['product_type'] == "SE IPS SCH40/DWV SOLID WALL PVC PLAIN OR BELLED END 20'", 'product_type'] = "PVC PIPE SCH 40 - BELL END"


df.loc[(df['product_type'] == "SCH 80 WATER PIPE 20 LENGTH") & (df['source'] == "jme_SolvetWeldLoadingChart_0"), 'product_type'] = "PVC PIPE SCH 80 - BELL END"

# Filter the rows that need to be duplicated

rows_to_duplicate = df[(df['product_type'] == "PVC PIPE SCH 40 - BELL END") & (~df['size'].isin(['10', '12']))].copy()

# Update the product_type of the new duplicated rows
rows_to_duplicate['product_type'] = "SDR13.5 BE - BELL END"

# Append the new rows to the original DataFrame
df = pd.concat([df, rows_to_duplicate], ignore_index=True)

# Create a DataFrame with unique product types
query = """
select 
    distinct
        product_type,
        source
from
    df
order by source, product_type
"""
df_product_type = duckdb.sql(query).df()
# Reset the index and add 1 to each index value
df_product_type.reset_index(inplace=True)
df_product_type['index'] = df_product_type['index'] + 1
# Rename the 'index' column to 'productTypeId'
df_product_type = df_product_type.rename(columns={'index': 'productTypeId'})
# Join the df_productType and df DataFrames based on productType
query = """
select
    df_product_type.productTypeId as productTypeId,
    df.*
from
    df_product_type,
    df
where
    df_product_type.product_type = df.product_type
    and df_product_type.source = df.source
"""
df_with_product_type_id = duckdb.sql(query).df()


# Step 1: Split rows based on comma in size
def split_size(row):
    if 'DR' in row['size'] and ',' in row['size']:
        base, sizes_part = row['size'].split(' DR ', 1)
        sizes = [f"{base} DR {s.strip()}" for s in sizes_part.split(',')]
        new_rows = []
        for size in sizes:
            new_row = row.copy()
            new_row['size'] = size
            new_rows.append(new_row)
        return new_rows
    else:
        return [row]

# Apply the size split function to each row
size_split_rows = []
for _, row in df_with_product_type_id.iterrows():
    size_split_rows.extend(split_size(row))

size_split_df = pd.DataFrame(size_split_rows)

size_split_df.reset_index(inplace=True)
size_split_df['index'] = size_split_df['index'] + 1
size_split_df = size_split_df.rename(columns={'index': 'skuId'})


# Step 2: Split rows based on slashes in pcs_lift and other relevant columns
def split_slashes(row):
    pcs_lift_list = row['pcs_lift'].split(' / ')
    ft_lift_list = row['ft_lift'].split(' / ')
    lifts_load_list = row['lifts_load'].split(' / ')
    load_percentage_list = row['load_percentage'].replace('%', '').split(' / ')

    new_rows = []
    for i in range(len(pcs_lift_list)):
        new_row = row.copy()
        new_row['pcs_lift'] = pcs_lift_list[i]
        new_row['ft_lift'] = ft_lift_list[i] if i < len(ft_lift_list) else ft_lift_list[-1]
        new_row['lifts_load'] = lifts_load_list[i] if i < len(lifts_load_list) else lifts_load_list[-1]
        new_row['load_percentage'] = load_percentage_list[i] if i < len(load_percentage_list) else load_percentage_list[-1]
        new_rows.append(new_row)
    return new_rows

# Apply the slash split function to each row
expanded_rows = []
for _, row in size_split_df.iterrows():
    expanded_rows.extend(split_slashes(row))

expanded_df = pd.DataFrame(expanded_rows)

# Create a DataFrame with unique product types
query_sku = """
select 
    distinct
        productTypeId,
        source
from
    expanded_df
order by source, product_type
"""
df_sku = duckdb.sql(query_sku).df()

expanded_df.reset_index(inplace=True)
expanded_df['index'] = expanded_df['index'] + 1
expanded_df = expanded_df.rename(columns={'index': 'bundleId'})

# Convert load_percentage back to string with '%' for consistency
expanded_df['load_percentage'] = expanded_df['load_percentage'].astype(str) + '%'

column_name ='popularityScore'
if column_name not in expanded_df.columns:
    expanded_df['popularityScore'] = np.nan



# If popularityScore is NaN, assign a random integer between 10 and 100
expanded_df['popularityScore'] = expanded_df['popularityScore'].apply(lambda x: x if pd.notna(x) else np.random.randint(10, 101))

# Apply the clean_string function to all columns
expanded_df = expanded_df.map(clean_string)

df_charts = expanded_df.copy(deep=True)

df_charts['product_type_active_flag'] = 'No'
df_charts['sku_active_flag'] = 'No'
df_charts['bundle_active_flag'] = 'No'

product_types_to_check = [
    "SDR35 PVC PIPE GRAVITY SEWER - GASKET", 
    "SDR26 PVC PIPE GRAVITY SEWER - GASKET", 
    "DR18 PVC PIPE C-900 - GASKET", 
    "SDR13.5 BE - BELL END",
    "PVC PIPE SCH 40 - BELL END",
    "PVC PIPE SCH 80 - BELL END",
]

# Update the flags for the specified product types
df_charts.loc[df_charts['product_type'].isin(product_types_to_check), ['product_type_active_flag', 'sku_active_flag', 'bundle_active_flag']] = 'Yes'

df_charts.loc[df_charts['size'].str.contains('West'), ['sku_active_flag', 'bundle_active_flag']] = 'No'


query_active = """
SELECT
    *
FROM
    df_charts
WHERE
 product_type_active_flag = 'Yes'




"""
df_active = duckdb.sql(query_active).df()

query_product_type = """
SELECT
    distinct 
    productTypeId as product_type_id,
    product_type_active_flag as active_flag,
    product_type as product_type,
    source
FROM
    df_charts
"""
product_type = duckdb.sql(query_product_type).df()

query_sku = """
SELECT
    distinct 
    skuId as SKU_id,
    productTypeId as product_type_id,
    product_type as product_type,
    sku_active_flag as active_flag,
    size,
    length,
    pcs_lift,
    ft_lift,
    lifts_load,
    load_percentage,
    ft_load,
    popularityScore as popularity_score,
    source
FROM
    df_charts
"""
sku = duckdb.sql(query_sku).df()

query_bundle = """
SELECT
    distinct
    bundleId as bundle_id,
    skuId as SKU_id,
    productTypeId as product_type_id,
    product_type as product_type,
    bundle_active_flag as active_flag,
    size,
    length,
    pcs_lift,
    ft_lift,
    lifts_load,
    load_percentage,
    ft_load,
    popularityScore as popularity_score,
    source
FROM
    df_charts
"""
bundle = duckdb.sql(query_bundle).df()

from sqlalchemy import create_engine, text
# Connection details
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'password'
mysql_database = 'h2o_loading_data'

# Create a SQLAlchemy engine
engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')


# List of tables to truncate
tables_to_truncate = ['bundle', 'sku', 'product_type']


# Truncate the tables
with engine.connect() as connection:
    for table in tables_to_truncate:
        connection.execute(text(f"TRUNCATE TABLE {table}"))
        print(f"Truncated table {table}")

# Insert data from the DataFrame into the product_type table
product_type.to_sql(name='product_type', con=engine, if_exists='append', index=False)
print("Product Type Data inserted successfully.")

# Insert data from the DataFrame into the product_type table
sku.to_sql(name='sku', con=engine, if_exists='append', index=False)
print("SKU Data inserted successfully.")

# Insert data from the DataFrame into the product_type table
bundle.to_sql(name='bundle', con=engine, if_exists='append', index=False)
print("Bundle Data inserted successfully.")


# Perform all actions in a single transaction
with engine.connect() as connection:
    transaction = connection.begin()
    try:
        # Truncate the tables
        for table in tables_to_truncate:
            connection.execute(text(f"TRUNCATE TABLE {table}"))
            print(f"Truncated table {table}")

        # Insert data into the product_type table
        product_type.to_sql(name='product_type', con=connection, if_exists='append', index=False)
        print("Product Type Data inserted successfully.")

        # Insert data into the sku table
        sku.to_sql(name='sku', con=connection, if_exists='append', index=False)
        print("SKU Data inserted successfully.")

        # Insert data into the bundle table
        bundle.to_sql(name='bundle', con=connection, if_exists='append', index=False)
        print("Bundle Data inserted successfully.")

        # Commit the transaction
        transaction.commit()
        print("All actions committed successfully.")
    except Exception as e:
        # Rollback the transaction in case of error
        transaction.rollback()
        print(f"Error: {e}")
    finally:
        connection.close()

# # Extract the size from the DESCRIPTION_1 column
# df['size'] = df['DESCRIPTION_1'].str.split('" ').str[0] + '"'

# # Apply the clean_string function to all columns
# df = df.map(clean_string)

# # Extract the productType from the DESCRIPTION_1 and DESCRIPTION_2 columns
# df['productType'] = df['DESCRIPTION_1'].str.split('"').str[1] + ' - ' + df['DESCRIPTION_2']

# # Drop the DESCRIPTION_1 and DESCRIPTION_2 columns
# df.drop(['DESCRIPTION_1','DESCRIPTION_2'], axis=1, inplace=True)

# # Apply the clean_string function to all columns
# df = df.map(clean_string)

# # Reset the index and add 1 to each index value
# df.reset_index(inplace=True)
# df['index'] = df['index'] + 1

# # Rename the 'index' column to 'skuId'
# df = df.rename(columns={'index': 'skuId'})

# # Create a DataFrame with unique product types
# query = """
# select 
#     distinct
#         productType
# from
#     df
# order by productType
# """
# df_productType = duckdb.sql(query).df()

# # Reset the index and add 1 to each index value
# df_productType.reset_index(inplace=True)
# df_productType['index'] = df_productType['index'] + 1

# # Rename the 'index' column to 'productTypeId'
# df_productType = df_productType.rename(columns={'index': 'productTypeId'})

# # Join the df_productType and df DataFrames based on productType
# query = """
# select
#     df_producttype.productTypeId as productTypeId,
#     df.*
# from
#     df_productType,
#     df
# where
#     df_productType.productType = df.productType
# """
# df_output = duckdb.sql(query).df()

# # Add prefixes to SKUId and productTypeId columns
# df_output['skuId'] = 'skuId_' + df_output['skuId'].astype(str)
# df_output['productTypeId'] = 'productTypeId_' + df_output['productTypeId'].astype(str)

# # Calculate bundlesPerTruckloadForCalculation
# df_output['bundlesPerTruckloadForCalculation'] = df_output['sticksPerTruckload'] / df_output['sticksPerBundleForCalculation']

# # Write the processed DataFrame to a CSV file
# df_output.to_csv(output_filename, index=False)  # Set index=False to exclude the row index
