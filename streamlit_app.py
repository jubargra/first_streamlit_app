import streamlit
import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# set index to 'Fruit' so users can pick a fruit instead of id when using the list in line 17
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('Breakfast Favorites')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice= streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# takes the json, normalizes it, stores in new variable 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# uses datraframe(variable) to display it in a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchone() 
my_data_row = my_cur.fetchall() # fetches all rows from fruit_load_list
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', '')
streamlit.write('Thanks for adding', add_my_fruit)

# this will not work
my_cur.execute("insert into fruit_load_list values('from streamlit')")


