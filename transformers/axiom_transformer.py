import pandas as pd

def transform_sales(exel_path, source_df):


    data = pd.read_excel(exel_path,sheet_name='Sales w37')
    axiom_column = 'Article_Axiom'
    
    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['ITEM']
            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[axiom_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'Axiom',
                    'Article': row['ITEM'],
                    'model': row['ITMDSC'],
                    'site name': row['Location'],
                    'sales': row['Sales'],
                    'Selling Price': row['Value'],
                })
            else:
                sales_data.append({
                    'barcode': row['BARCODE'],
                    'model': row['ITMDSC'],
                    'Retail': 'Axiom',
                    'site id': None,
                    'site name': row['Location'],
                    'sales': row['Sales'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                    'Color': None
                })


    
    return sales_data, non_defined_items


def transform_stocks(exel_path, source_df):


    data = pd.read_excel(exel_path,sheet_name='Stock',header=[1])
    axiom_column = 'Article_Axiom'
    
    stock_list = []
    non_defined_list = []
    data.columns = data.columns.str.strip()
    source_df.columns = source_df.columns.str.strip()
    if data is not None:
        for index, row in data.iterrows():
         
            

            desired_value = row['PRODUCT CODE']
            
            
            
            filtered_df = source_df[source_df[axiom_column] == desired_value]

            if filtered_df.empty:
                non_defined_list.append({
                    'Retail': 'Axiom',
                    'Article': row['PRODUCT CODE'],
                    'model': row['PRODUCT DESCRIPTION'],
                    'stock': row['SOH'],
                })
            else:
                stock_list.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'Retail': 'Axiom',
                    'Article': row['PRODUCT CODE'],
                    'model': row['PRODUCT DESCRIPTION'],
                    'stock': row['SOH'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                })



    return stock_list, non_defined_list