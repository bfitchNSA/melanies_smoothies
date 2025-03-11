# Import python packages
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! 🍒")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input for smoothie name
NAME_ON_ORDER = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', NAME_ON_ORDER)

# Snowflake Connection
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Fetch available fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
fruit_list = my_dataframe["FRUIT_NAME"].tolist()

# Multiselect for ingredient choices
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)

# Handle submission
if ingredients_list and NAME_ON_ORDER:
    ingredients_string = ', '.join(ingredients_list)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
    VALUES (?, ?)
    """
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, NAME_ON_ORDER]).collect()
        st.success(f'Your Smoothie is ordered, {NAME_ON_ORDER}! ✅')

