import pandas as pd
def transform_sales(exel_path, source_df):
    data = pd.read_excel(exel_path,header=[0,1],sheet_name='Sheet1',)
    target_column = 'Article_Dubai_Duty_Free'

    sales_data = []
    non_defined_items = []


    if data is not None:

        for index, row in data.iterrows():

            desired_value = row['RIN'].values[0]
          

            source_df.columns = source_df.columns.str.strip()

            filtered_df = source_df[source_df[target_column] == desired_value]
            quantity_per_location = {
                "CC":float(row['MTD']['CC']),
                "CB":float(row['MTD']['CB']),
                "T2":float(row['MTD']['T2']),
                "CA":float(row['MTD']['CA']),
                "CD":float(row['MTD']['CD']),
                "DW":float(row['MTD']['DW']),
            }

            
            sell_price = 0
            if float(row['MTD']['∑']) > 0:
                sell_price = float(row['MTD']['Value']) / row['MTD']['∑']

            if filtered_df.empty:

                for location, quantity in quantity_per_location.items():
                    if quantity > 0:
                        non_defined_items.append({
                            'Retail': 'Dubai_Duty_Free',
                            'Item': row['DESCRIPTION'].values[0],
                            'site name': location,
                            'sales':quantity,
                            'Selling Price': sell_price,
                        })


            else:
                for location, quantity in quantity_per_location.items():
                    if quantity > 0:
                        sales_data.append({
                            'barcode': filtered_df['Barcode'].values[0],
                            'model': row['DESCRIPTION'].values[0],
                            'Retail': 'Dubai_Duty_Free',
                            'site id': None,
                            'site name': location,
                            'sales': quantity,
                            'Selling Price': sell_price,
                            'Color': None
                        })



    return sales_data, non_defined_items