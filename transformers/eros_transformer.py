import pandas as pd
def transform_sales(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='SALES',)
    target_column = 'Article_Eros'

    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['Item code']
            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'Eros',
                    'Article': row['Item code'],
                    'model': row['Item code'],
                    'site name': row['Location'],
                    'sales':row['QTY']
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'model': row['Item code'],
                    'Retail': 'Eros',
                    'site id': None,
                    'site name': row['Location'],
                    'sales': row['QTY'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                    'Color': None
                })



    return sales_data, non_defined_items