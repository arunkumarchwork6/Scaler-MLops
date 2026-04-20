import streamlit as st
import pandas as pd

st.title("this is title")
st.header("this is header")
st.subheader("A subtitle")
st.write("hello Arun")

df = pd.DataFrame(
    {"id":[1,2,3,4],
    "name" : ['arun','sandeep','prathysha','samata']
    }
)

st.dataframe(df)

def sqr(num):
	
	return num*num


num = int(st.number_input('Insert a number'))

# display the name when the submit button is clicked
# .title() is used to get the input text string


if(st.button("Calculate Square")):
    result = sqr(num)
    st.text(result)

