# app.py
import streamlit as st
import pandas as pd
from streamlit_extras.grid import grid
from mystuff import *
from data_reader import *
from transormer import *
from transformers import transform_sales,transform_stock
# Hardcoded username and password for demonstration purposes
USERNAME = "user"
PASSWORD = "password"
# array of objects of store datas

files={}
stores_list = [
    {
        'title' : "Axiom",
        'slug' : "axiom",
        'input_type' :"exel",

    },
    {
        'title' : "Dubai_Duty",
        'slug' : "dubai_duty",
        'input_type' :"exel",
    },
    {
        'title' : "Eros",
        'slug' : "eros",
        'input_type' :"exel",
    },
    {
    
        'title' : "E-city",
        'slug' : "e_city",
        'input_type' :"exel",
    },
    {
    
        'title' : "Jackys",
        'slug' : "jackys",
        'input_type' :"exel",
    },
    {
    
        'title' : "Nesto Xiaomi",
        'slug' : "nesto_xiaomi",
        'input_type' :"exel",
    },
    {
    
        'title' : "Nesto Lazor",
        'slug' : "nesto_lazor",
        'input_type' :"exel",
    }
    
]
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['step'] = "register"
    # cache goes here

    if 'app_cache' not in st.session_state:
        st.session_state['app_cache'] = True
        
        st.session_state['lulu_array'] = []
        st.session_state['lulu_sales_transformed_data'] = []
        st.session_state['lulu_stocks_transformed_data'] = []
        st.session_state['lulu_nondef_transformed_data'] = []
        
        st.session_state['c4_sales_array'] = []
        st.session_state['c4_stocks_array'] = []
        st.session_state['c4_sales_transformed_data'] = []
        st.session_state['c4_stocks_transformed_data'] = []
        
        st.session_state['sdg_sales_array'] = []
        st.session_state['sdg_stocks_array'] = []
        st.session_state['sdg_sales_transformed_data'] = []
        st.session_state['sdg_nondef_sales_transformed_data'] = []
        st.session_state['sdg_stocks_transformed_data'] = []
        st.session_state['sdg_nondef_stocks_transformed_data'] = []

        for store in stores_list :
            st.session_state[store['slug']+'_sales'] = []
            st.session_state[store['slug']+'_stocks'] = []
            st.session_state[store['slug']+'_stock_transformed_data'] = []
            st.session_state[store['slug']+'_sales_transformed_data'] = []
            st.session_state[store['slug']+'_nondef_transformed_data'] = []
            st.session_state[store['slug']+'_nondef_stocks_transformed_data'] = []



        st.session_state['dubai_duty_sales'] = []
        st.session_state['dubai_duty_stocks'] = []
        st.session_state['dubai_duty_stock_transformed_data'] = []
        st.session_state['dubai_duty_sales_transformed_data'] = []
        st.session_state['dubai_duty_nondef_transformed_data'] = []

        st.session_state['source_df'] = pd.DataFrame()
        
        st.session_state['all_sales'] = []
        st.session_state['all_stocks'] = []
        st.session_state['all_nondef'] = []
        
        st.session_state['all_sales_df'] = pd.DataFrame()
        st.session_state['all_stocks_df'] = pd.DataFrame()
        st.session_state['all_nondef_df'] = pd.DataFrame()
        
        st.session_state['Step'] = 0
        st.session_state['output'] = ""


def login():
    st.title("Login Page")

    # Get user inputs
    entered_username = st.text_input("Username:")
    entered_password = st.text_input("Password:", type="password")

    # Check if the entered credentials are correct
    if st.button("Login"):
        if entered_username == USERNAME and entered_password == PASSWORD:
            st.success("Login successful!")
            st.session_state['logged_in'] = True
            st.experimental_rerun()

def logout():
    st.session_state['logged_in'] = False
    st.experimental_rerun()



if st.session_state['logged_in']:
    with st.sidebar:
        if st.button("Logout"):
            logout()
            
            
    # MAIN PAGE        
    with st.container():
        st.title("TaskMi Data Reporting System")
        # code goes here

        st.title("Control Panel")

        if st.session_state['Step'] == 0:
            pass
        elif  st.session_state['Step'] == 1:
            store_titles = tuple([store['title'] for store in stores_list])
            st.session_state['output'] = st.selectbox(
                "Output Data",
                # ("Carrefour", "SharafDG", "LuLu", "Axiom","Dubai_Duty","Nesto","Eros", "All"),
                ("Carrefour", "SharafDG", "LuLu", "Axiom","Dubai_Duty","Eros","E-city","Jackys","Nesto Xiaomi","Nesto Lazor", "All"),
                index=3,
                )
            
            st.download_button(
                    label="Download Sales data as CSV",
                    data=pd.DataFrame(st.session_state.all_sales).to_csv().encode('utf-8'),
                    file_name='all_sales_df.csv',
                    mime='text/csv',
                )
            st.download_button(
                    label="Download Stocks data as CSV",
                    data=pd.DataFrame(st.session_state.all_stocks).to_csv().encode('utf-8'),
                    file_name='all_stocks_df.csv',
                    mime='text/csv',
                )
            st.download_button(
                    label="Download Non-Defined data as CSV",
                    data=pd.DataFrame(st.session_state.all_nondef).to_csv().encode('utf-8'),
                    file_name='all_nondef_df.csv',
                    mime='text/csv',
                )
    
    
    # --- MAIN PAGE ---
    with st.container():
        
        if  st.session_state['Step'] == 0:

            with st.form("Data Input"):

                layout = grid(1,[1,3],1,1,[1,3],1,1,[1,3],[1,3],1,1,[1,3],[1,3],[1,3],1,[1,3],1,[1,3],1,[1,3],1,[1,3],1,[1,3], vertical_align="bottom")
                
                layout.write("## Source")
                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcannaangelsllc.com%2Fwp-content%2Fuploads%2F2015%2F02%2Fplace-holder-image.png&f=1&nofb=1&ipt=b1b6b10c6455a7b6c13e704f2b5ebf46c7e89c6fa5c5bbf08c06bc393fc1c95d&ipo=images")
                source_csv = layout.file_uploader("Source file:")

                layout.write("---")

                layout.write("## LuLu")
                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdubaiofw.com%2Fwp-content%2Fuploads%2F2020%2F08%2FLulu-Group.jpg&f=1&nofb=1&ipt=f88410766403a882867373e7f055cc3df0c0d4126f36ac1a3b6feb798b42285b&ipo=images")
                lulu_csv = layout.file_uploader("CSV:")

                layout.write("---")
                
                layout.write("## Carrefour")
                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fk1fRCbBYfPU%2Fmaxresdefault.jpg&f=1&nofb=1&ipt=d62ccbe9dd3fc6e050a04fcf8b474b5244bd86316dc55f108e8dc58cc9a82ecf&ipo=images")
                c4_stock_xlsb = layout.file_uploader("Stock XLSB:")

                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fk1fRCbBYfPU%2Fmaxresdefault.jpg&f=1&nofb=1&ipt=d62ccbe9dd3fc6e050a04fcf8b474b5244bd86316dc55f108e8dc58cc9a82ecf&ipo=images")
                c4_sales_xlsb = layout.file_uploader("Sales XLSB:")
                
                layout.write("---")
                layout.write("## SharafDG")
                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fplay-lh.googleusercontent.com%2FtOfRUO9ngWCHUfJ9xuakVtFif1q1jostzDGE4DwT9MZOCV9y3kgRX_l0o_GvS1ueOzSo%3Dw720-h310&f=1&nofb=1&ipt=05c264fceefb9807b8b9cc0ea297647aca033d343218e948ae53abc0bf692723&ipo=images")
                
                sdg_stock_csv = layout.file_uploader("Stock CSV:")
                layout.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fplay-lh.googleusercontent.com%2FtOfRUO9ngWCHUfJ9xuakVtFif1q1jostzDGE4DwT9MZOCV9y3kgRX_l0o_GvS1ueOzSo%3Dw720-h310&f=1&nofb=1&ipt=05c264fceefb9807b8b9cc0ea297647aca033d343218e948ae53abc0bf692723&ipo=images")
                sdg_sales_csv = layout.file_uploader("Sales CSV:")

                for store in stores_list :
                    layout.write("---")

                    layout.write("## "+store['title'])
                    # layout.image("https://pbs.twimg.com/profile_images/471600164700839936/teX8RIvJ_400x400.png")
                    files[store['slug']] = layout.file_uploader(store['title']+" Sales CSV:")


                layout.write("---")

                
                # layout.write("---")

                # layout.write("## Eros")
                # # layout.image("https://pbs.twimg.com/profile_images/471600164700839936/teX8RIvJ_400x400.png")
                # eros_stock_csv = layout.file_uploader("Eros Stock CSV:")
                
                # layout.write("---")
                # layout.write("## Nesto")
                # # layout.image("https://pbs.twimg.com/profile_images/471600164700839936/teX8RIvJ_400x400.png")
                # nesto_stock_csv = layout.file_uploader("Nesto Stock CSV:")



                if st.form_submit_button("Clean Data...", use_container_width=True):
                    # for store in stores_list :
                    #     if files[store['slug']] is not None:
                    #         st.session_state[store['slug']+'_sales'] = pd.read_excel(files[store['slug']], sheet_name=store['sheet_name'])
                    #     else:
                    #         st.session_state[store['slug']+'_sales'] = None



                    if lulu_csv is not None:
                        st.session_state['lulu_array'] = Lulu(lulu_csv)
                    else:
                        st.session_state['lulu_array'] = None
                    
                    if c4_stock_xlsb is not None:
                        st.session_state['c4_stocks_array'] = C4_stock(c4_stock_xlsb)
                    else:
                        st.session_state['c4_stocks_array'] = None

                    if c4_sales_xlsb is not None:
                        st.session_state['c4_sales_array'] = C4_sales(c4_sales_xlsb)
                    else:
                        st.session_state['c4_sales_array'] = None

                    if sdg_stock_csv is not None:
                        st.session_state['sdg_stocks_array'] = SDG_stock(sdg_stock_csv)
                    else:
                        st.session_state['sdg_stocks_array'] = None

                    if sdg_sales_csv is not None:
                        st.session_state['sdg_sales_array'] = SDG_sales(sdg_sales_csv)
                    else:
                        st.session_state['sdg_sales_array'] = None

                    if source_csv is not None:
                        st.session_state['source_df'] = pd.read_csv(source_csv)
                    else:
                        st.session_state['source_df'] = None

                    
                    st.session_state['lulu_sales_transformed_data'], st.session_state['lulu_stocks_transformed_data'], st.session_state['lulu_nondef_transformed_data'] = transform_data_LULU( st.session_state['lulu_array'] ,st.session_state['source_df'])
                    st.session_state['sdg_sales_transformed_data'], st.session_state['sdg_nondef_sales_transformed_data'] = transform_data_SDG_sales(st.session_state['sdg_sales_array'] ,st.session_state['source_df'])
                    st.session_state['sdg_stocks_transformed_data'], st.session_state['sdg_nondef_stocks_transformed_data'] = transform_data_SDG_stock(st.session_state['sdg_stocks_array'] ,st.session_state['source_df'])
                    st.session_state['c4_stocks_transformed_data'] = transform_data_C4_stock(st.session_state['c4_stocks_array'] ,st.session_state['source_df'])
                    st.session_state['c4_sales_transformed_data'] = transform_data_C4_sales(st.session_state['c4_sales_array'] ,st.session_state['source_df'])

                    for store in stores_list:
                        if files[store['slug']] is not None:
                            st.session_state[store['slug']+'_sales_transformed_data'], st.session_state[store['slug']+'_nondef_transformed_data'] = transform_sales(store['slug'],files[store['slug']] ,st.session_state['source_df'])
                            st.session_state[store['slug']+'_stock_transformed_data'], st.session_state[store['slug']+'_nondef_stocks_transformed_data'] = transform_stock(store['slug'],files[store['slug']] ,st.session_state['source_df'])

                        # st.session_state[store['slug']+'_sales_transformed_data'], st.session_state[store['slug']+'_nondef_transformed_data'] = transformer_data_axiom_sales(st.session_state[store['slug']+'_sales'] ,st.session_state['source_df'])


                    print(st.session_state['axiom_sales_transformed_data'])

                    ### Sales
                    for item in st.session_state['lulu_sales_transformed_data']:
                        st.session_state['all_sales'].append(item)

                    for item in st.session_state['c4_sales_transformed_data']:
                        st.session_state['all_sales'].append(item)

                    for item in st.session_state['sdg_sales_transformed_data']:
                        st.session_state['all_sales'].append(item)
                    #multiple sales
                    for store in stores_list:
                        for item in st.session_state[store['slug']+'_sales_transformed_data']:
                            st.session_state['all_sales'].append(item)

                    ### Stock
                    for item in st.session_state['lulu_stocks_transformed_data']:
                        st.session_state['all_stocks'].append(item)

                    for item in st.session_state['c4_stocks_transformed_data']:
                        st.session_state['all_stocks'].append(item)

                    for item in st.session_state['sdg_stocks_transformed_data']:
                        st.session_state['all_stocks'].append(item)
                    

                    ### Non-Def
                    for item in st.session_state['lulu_nondef_transformed_data']:
                        st.session_state['all_nondef'].append(item)

                    for item in st.session_state['sdg_nondef_sales_transformed_data']:
                        st.session_state['all_nondef'].append(item)

                    for item in st.session_state['sdg_nondef_sales_transformed_data']:
                        st.session_state['all_nondef'].append(item)
                    
                    #multiple Nondef
                    for store in stores_list:
                        for item in st.session_state[store['slug']+'_nondef_transformed_data']:
                            st.session_state['all_nondef'].append(item)

                    # for item in st.session_state['eros_nondef_transformed_data']:
                    #     st.session_state['all_nondef'].append(item)

                    # for item in st.session_state['nesto_nondef_transformed_data']:
                    #     st.session_state['all_nondef'].append(item)

                    # for item in st.session_state['dubai_duty_nondef_transformed_data']:
                    #     st.session_state['all_nondef'].append(item)
                        
                    st.session_state['Step'] = 1
                    st.experimental_rerun()
                    
        elif st.session_state['Step'] == 1:

            if st.button("Back to Upload"):
                st.session_state['Step'] = 0
                st.session_state['all_sales'] = []
                st.session_state['all_stocks'] = []
                st.session_state['all_nondef'] = []
                st.experimental_rerun()
            
            if st.session_state['output'] == "All":

                st.write("# All Sales Data:")
                st.dataframe(st.session_state.all_sales)

                st.write("# All Stocks Data:")
                st.dataframe(st.session_state.all_stocks)

                st.write("# All Non-Defined Data:")
                st.dataframe(st.session_state.all_nondef)
            
            elif st.session_state['output'] == "Carrefour":
                st.write("# Carrefour Sales Data:")
                st.dataframe(st.session_state['c4_sales_transformed_data'])
                st.write("# Carrefour Stocks Data:")
                st.dataframe(st.session_state['c4_stocks_transformed_data'])
            
            elif st.session_state['output'] == "SharafDG":
                st.write("# SharafDG Sales Data:")
                st.dataframe(st.session_state['sdg_sales_transformed_data'])
                st.write("# SharafDG Stocks Data:")
                st.dataframe(st.session_state['sdg_stocks_transformed_data'])
                st.write("# SharafDG Non-Defined Data:")
                st.dataframe(st.session_state['sdg_nondef_sales_transformed_data'])
                st.dataframe(st.session_state['sdg_nondef_stocks_transformed_data'])
            
            elif st.session_state['output'] == "LuLu":
                st.write("# LuLu Sales Data:")
                st.dataframe(st.session_state['lulu_sales_transformed_data'])
                st.write("# LuLu Stocks Data:")
                st.dataframe(st.session_state['lulu_stocks_transformed_data'])
                st.write("# LuLu Non-Defined Data:")
                st.dataframe(st.session_state['lulu_nondef_transformed_data'])

            else:
                for store in stores_list:
                    if st.session_state['output'] == store['title']:
                        st.write(store['title']+" Sales Data:")
                        st.dataframe(st.session_state[store['slug']+'_sales_transformed_data'])
                        st.write(store['title']+" Stocks Data:")
                        st.dataframe(st.session_state[store['slug']+'_stock_transformed_data'])
                        # st.dataframe(st.session_state['axiom_stocks_transformed_data'])
                        st.write(store['title']+" Non-Defined Sales:")
                        st.dataframe(st.session_state[store['slug']+'_nondef_transformed_data'])


            # st.dataframe(data=st.session_state['all_sales_df'])
        

            # st.dataframe(data=st.session_state['all_sales_df'])
        

    
    
    
    
    
if st.session_state['logged_in']==False:
    st.session_state['logged_in']=True
    st.experimental_rerun()
    # login()