import streamlit as st
import numpy as np
import pandas as pd

# ---- STEP 1 FUNCTIONS -----
def Lulu(file_path):
    import pandas as pd
    import re
    
    def clean_qty_value(value):
        # Extract the number inside square brackets or parentheses
        match = re.search(r'[\[\(](\d+)[\]\)]', str(value))
        if match:
            return match.group(1)
        return value

    # Load the CSV file into a dataframe, excluding the last 2 rows
    df = pd.read_csv(file_path, skipfooter=2, engine='python')
    
    # Extract the Plant IDs and Names
    plant_ids = df.iloc[1, 2:].values
    plant_names = df.iloc[2, 2:].values
    
    # Prepare the list of dictionaries
    data_list = []

    for i, row in df.iterrows():
        if i < 5:  # Skip the header rows
            continue

        # Material and Material Name
        material = row['Unnamed: 1']
        material_name = row['Purchasing Org.']

        # Iterate through the columns
        j = 2
        while j < df.shape[1] - 1:
            # Check for valid Plant ID
            if pd.notna(plant_ids[j - 2]) and str(plant_ids[j - 2]).isdigit():
                
                # Plant ID and Name for the current column
                plant_id = plant_ids[j - 2]
                plant_name = plant_names[j - 2]
                
                # Extract Sales Qty and Stock Qty with cleaning step
                sales_qty = clean_qty_value(row[j])
                stock_qty = clean_qty_value(row[j + 1])
                
                # Add the data to the list of dictionaries
                data_list.append({
                    'Material': material,
                    'Material Name': material_name,
                    'Plant ID': plant_id,
                    'Plant Name': plant_name,
                    'Sales Qty': sales_qty if not pd.isna(sales_qty) else 'N/A',
                    'Stock Qty': stock_qty if not pd.isna(stock_qty) else 'N/A'
                })

                j += 2  # Move to the next column
            else:
                j += 1  # Skip the current column

    return data_list

def SDG_sales(file_path):
    try:
        # Read specific columns from the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, usecols=["SKU", "Site Code", "Site Description", "Sold"])
        
        # Convert DataFrame to list of dictionaries
        list_of_dicts = df.to_dict(orient='records')
        
        # Return the list of dictionaries
        return list_of_dicts
    
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def SDG_stock(file_path):
    try:
        # Read specific columns from the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, usecols=["SKU", "Site Code", "Site Description", "SOH"])
        
        # Convert DataFrame to list of dictionaries
        list_of_dicts = df.to_dict(orient='records')
        
        # Return the list of dictionaries
        return list_of_dicts
    
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def C4_sales(file_path):
    # Load the excel file into a DataFrame
    df = pd.read_excel(file_path, engine='pyxlsb')

    # Initialize an empty list to store the dictionaries
    data_list = []

    # Loop through each row of the DataFrame
    for _, row in df.iterrows():
        # Extract barcode and item description
        barcode = row['BARCODE']
        itmdsc = row['ITMDSC']

        # Loop through store columns (excluding 'PCB' and 'TOTAL')
        for col in df.columns[19:56]:  # Starting from column T to BB
            store_name = col
            sales_qty = row[col]

            # Create a dictionary and append to the list
            data_dict = {
                'BARCOD': barcode,
                'ITMDSC': itmdsc,
                'store name': store_name,
                'Sales Qty': sales_qty if not pd.isna(sales_qty) else 'N/A'
            }

            data_list.append(data_dict)

    return data_list

def C4_stock(filepath: str) -> list:
    """
    Extract Stock on Hand (SOH) data from the provided Excel file.
    
    Parameters:
    - filepath (str): Path to the Excel file.
    
    Returns:
    - list: List of dictionaries containing BARCOD, ITMDSC, store name, and Stock Qty.
    """
    # Load the excel file into a dataframe
    df = pd.read_excel(filepath, engine='pyxlsb')

    # Extract the store names from the first row
    store_columns = df.columns[17:54]  # Columns R to BB based on the displayed data

    # Initialize the result list
    result = []

    # Loop through each store column
    for store in store_columns:
        for index, row in df.iterrows():
            data_dict = {
                'BARCOD': int(row['BARCOD']),
                'ITMDSC': row['ITMDSC'],
                'store name': store,
                'Stock Qty': row[store]
            }
            result.append(data_dict)

    return result

def Axiom_stock(file_path):
    try:
        # Read specific columns from the CSV file into a pandas DataFrame
        df = pd.read_excel(file_path)
        
        # Convert DataFrame to list of dictionaries
        list_of_dicts = df.to_dict(orient='records')
        
        # Return the list of dictionaries
        return list_of_dicts
    
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None