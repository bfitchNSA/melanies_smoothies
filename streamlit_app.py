# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("Customize Your Smoothie!:cherries:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)


NAME_ON_ORDER= st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', NAME_ON_ORDER)

cnx = st. connection ("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function pd_df=my_dataframe.to_pandas()
pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df, use_container_width=True)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''
   
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The Search value for', fruit_chosen, 'is', search_on)

        st.subheader(fruit_chosen + 'Nutritional Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+NAME_ON_ORDER+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
    st.success(f'Your Smoothie is ordered, {NAME_ON_ORDER}', icon="✅")





