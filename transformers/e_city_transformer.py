import pandas as pd
def transform_sales(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='Sellout',)
    target_column = 'Article_E_City'

    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['Article']
            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'E-City',
                    'Article': row['Article'],
                    'model': row['Article Name'],
                    'site name': row['Site Name'],
                    'sales':row['SO QTY']
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'model': row['Article Name'],
                    'Retail': 'E-city',
                    'site id': row['Site'],
                    'site name': row['Site Name'],
                    'sales': row['SO QTY'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                    'Color': None
                })



    return sales_data, non_defined_items


def transform_stocks(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='SOH',)
    target_column = 'Article_E_City'

    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['Article']
            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'E-City',
                    'Article': row['Article'],
                    'model': row['Article Description'],
                    'stock': row['Total Qty'],
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'Retail': 'E-City',
                    'Article': row['Article'],
                    'model': row['Article Description'],
                    'stock': row['Total Qty'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                })



    return sales_data, non_defined_items