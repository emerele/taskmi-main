import pandas as pd

def transform_data_LULU(data_LULU, source_df):
    sales_data = []
    stock_data = []
    non_defined_items = []
    if data_LULU is not None:
        for item in data_LULU:
            # Match against source.csv using the Article_Lulu column
            
            try:
                material_float = float(item['Material'])
            except ValueError:
                # If not, add to non_defined_items and continue to next item
                non_defined_items.append({
                    'Retail': 'LULU',
                    'Item number': item['Material']
                })
                continue
            match = source_df[source_df['Article_Lulu'] == material_float]
            # If a match is found, create the required dictionaries for sales and stock
            if not match.empty:
                matched_data = match.iloc[0]
                if item['Sales Qty'] != 'N/A':
                    sales_data.append({
                        'barcode': matched_data['Barcode'],
                        'model': matched_data['Model'],
                        'Retail': 'LULU',
                        'site id': item['Plant ID'],
                        'site name': item['Plant Name'],
                        'sales': item['Sales Qty'],
                        'Selling Price': matched_data['Selling Price'],
                        'Color': matched_data['Color']
                    })
                if item['Stock Qty'] != 'N/A':
                    stock_data.append({
                        'barcode': matched_data['Barcode'],
                        'model': matched_data['Model'],
                        'Retail': 'LULU',
                        'site id': item['Plant ID'],
                        'site name': item['Plant Name'],
                        'stock': item['Stock Qty'],
                        'Selling Price': matched_data['Selling Price'],
                        'Color': matched_data['Color']
                    })
            else:
                # If no match is found, add to the non-defined item numbers list
                non_defined_items.append({
                    'Retail': 'LULU',
                    'Item number': item['Material']
                })
        
    return sales_data, stock_data, non_defined_items

def transform_data_SDG_sales(data_SDG_sales, source_df):
    sales_data = []
    non_defined_items = []
    
    if data_SDG_sales is not None:
        for item in data_SDG_sales:
            match = source_df[source_df['Article_DG'] == float(item['SKU'])]
            if not match.empty:
                matched_data = match.iloc[0]
                sales_data.append({
                    'barcode': matched_data['Barcode'],
                    'model': matched_data['Model'],
                    'Retail': 'SDG',
                    'site id': item['Site Code'],
                    'site name': item['Site Description'],
                    'sales': item['Sold'],
                    'Selling Price': matched_data['Selling Price'],
                    'Color': matched_data['Color']
                })
            else:
                non_defined_items.append({
                    'Retail': 'SDG',
                    'Item number': item['SKU']
                })

    return sales_data, non_defined_items

def transform_data_SDG_stock(data_SDG_stock, source_df):
    stock_data = []
    non_defined_items = []

    if data_SDG_stock is not None:
        for item in data_SDG_stock:
            match = source_df[source_df['Article_DG'] == float(item['SKU'])]
            if not match.empty:
                matched_data = match.iloc[0]
                stock_data.append({
                    'barcode': matched_data['Barcode'],
                    'model': matched_data['Model'],
                    'Retail': 'SDG',
                    'site id': item['Site Code'],
                    'site name': item['Site Description'],
                    'stock': item['SOH'],
                    'Selling Price': matched_data['Selling Price'],
                    'Color': matched_data['Color']
                })
            else:
                non_defined_items.append({
                    'Retail': 'SDG',
                    'Item number': item['SKU']
                })
        
    return stock_data, non_defined_items

def transform_data_C4_sales(data_C4_sales, source_df):
    sales_data = []

    if data_C4_sales is not None:
        for item in data_C4_sales:
            match = source_df[source_df['Barcode'] == item['BARCOD']]
            if not match.empty:
                matched_data = match.iloc[0]
                sales_data.append({
                    'barcode': matched_data['Barcode'],
                    'model': matched_data['Model'],
                    'Retail': 'C4',
                    'site id': None,
                    'site name': item['store name'],
                    'sales': item['Sales Qty'],
                    'Selling Price': matched_data['Selling Price'],
                    'Color': matched_data['Color']
                })
    
    return sales_data

def transform_data_C4_stock(data_C4_stock, source_df):
    stock_data = []

    if data_C4_stock is not None:
        for item in data_C4_stock:
            match = source_df[source_df['Barcode'] == item['BARCOD']]
            if not match.empty:
                matched_data = match.iloc[0]
                stock_data.append({
                    'barcode': matched_data['Barcode'],
                    'model': matched_data['Model'],
                    'Retail': 'C4',
                    'site id': None,
                    'site name': item['store name'],
                    'stock': item['Stock Qty'],
                    'Selling Price': matched_data['Selling Price'],
                    'Color': matched_data['Color']
                })
    
    return stock_data

def transformer_data_axiom_sales(data, source_df):

    sales_data = []
    non_defined_items = []

    axiom_column = 'Article_Axiom'

    for index, row in data.iterrows():

        desired_value = row['ITEM']
        source_df.columns = source_df.columns.str.strip()

        filtered_df = source_df[source_df[axiom_column] == desired_value]

        if filtered_df.empty:
            non_defined_items.append({
                'Retail': 'Axiom',
                'Item number': row['ITEM']
            })
        else:
            sales_data.append({
                'barcode': row['BARCODE'],
                'model': row['ITMDSC'],
                'Retail': 'Axiom',
                'site id': None,
                'site name': row['Location'],
                'sales': row['Sales'],
                'Selling Price': row['Value'],
                'Color': None
            })



    return sales_data, non_defined_items

def transformer_data_axiom_stock(data, source_df):

    stock_data = []

    axiom_column = 'Article_Axiom'

    for index, row in data.iterrows():
        
        desired_value = row['PRODUCT CODE']

        source_df.columns = source_df.columns.str.strip()

        filtered_df = source_df[source_df[axiom_column] == desired_value]

        if filtered_df.empty:
            pass
        else:
            stock_data.append({
                'barcode': filtered_df['Barcode'].values[0],
                'model': row['MODEL LONG DESCRIPTION'],
                'Retail': 'Axiom',
                'site id': None,
                'site name': None,
                'stock': row['SOH'],
                'Selling Price': None,
                'Color': None
            })

    return stock_data
