import streamlit as st


# Write directly to the app
st.title("Customize Your Smoothie!:cherries:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

NAME_ON_ORDER = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', NAME_ON_ORDER)

# Assuming the connection is handled elsewhere

session = cnx.session()  # Retrieve the session object

# Get the list of fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Display the list of fruits in a multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Combine ingredients into a string

    # Prepare SQL query using parameterized queries to avoid SQL injection
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
        VALUES (%s, %s)
    """

    # Button to submit the order
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        # Execute the query with the parameters safely
        with cnx.cursor() as cursor:
            cursor.execute(my_insert_stmt, (ingredients_string, NAME_ON_ORDER))

        # Success message after the order is placed
        st.success(f'Your Smoothie is ordered, {NAME_ON_ORDER}', icon="✅")
