import pandas as pd
def transform_sales(exel_path, source_df):
    data = pd.read_excel(exel_path,sheet_name='SELLOUT',)
    target_column = 'Article_Jackys'

    sales_data = []
    non_defined_items = []


    if data is not None:
        for index, row in data.iterrows():

            desired_value = row['ItemCode']
            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]

            if filtered_df.empty:
                non_defined_items.append({
                    'Retail': 'Jackys',
                    'Item': row['ItemCode'],
                    'site name': row['Location'],
                    'sales':row['Qty']
                })
            else:
                sales_data.append({
                    'barcode': filtered_df['Barcode'].values[0],
                    'model': row['ItemDesc'],
                    'Retail': 'Jackys',
                    'site id': None,
                    'site name': row['Location'],
                    'sales': row['Qty'],
                    'Selling Price': filtered_df['Selling Price'].values[0],
                    'Color': None
                })



    return sales_data, non_defined_items