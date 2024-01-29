
import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Moms New Healthy Diner');

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast');

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  # write your own comment -what does the next line do? 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

  

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information")
  else: 
    back_from_function= get_fruityvice_data(fruit_choice)
    # write your own comment - what does this do?
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()



streamlit.write('The user entered ', fruit_choice)



streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_fruit_load_list() : 
  with my_cnx.cursor() as my_cur:
       my_cur.execute("SELECT * FROM fruit_load_list")
       return my_cur.fetchall()


if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
  my_data_rows=get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)



def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO fruit_load_list VALUES ('"+ new_fruit +"')")
  return ("Thanks for adding "+ new_fruit)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')

if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
  back_from_function=insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)









  

