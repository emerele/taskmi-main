import pandas as pd
def transform_sales(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='Sales Report ',header=[3])
    target_column = 'Article_Nesto'

    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['Article']

            if pd.isna(row['Article']):
                continue


            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'Nesto',
                    'Article': row['Article'],
                    'model': row[5],
                    'site name': row[3],
                    'sales':row['EA'],
                    'selling price':row['AED'],
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'model': row[5],
                    'Retail': 'Nesto',
                    'site id': row['Site'],
                    'site name': row[3],
                    'sales': row['EA'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                    'Color': None
                })



    return sales_data, non_defined_items


def transform_stocks(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='Stock Report ')
    target_column = 'Article_Nesto'

    sales_data = []
    non_defined_items = []

    data.columns = data.columns.str.strip()
    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['Article']

            if pd.isna(row['Article']):
                continue


            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'Nesto',
                    'Article': row['Article'],
                    'model': row['Description'],
                    'stock': row['Total Stock']
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'Retail': 'Nesto',
                    'Article': row['Article'],
                    'model': row['Description'],
                    'stock': row['Total Stock'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                })



    return sales_data, non_defined_items