import streamlit as st
import pandas as pd

tabel=pd.DataFrame({"Comlumn 1":[0,1,2,3,4,5,6],"Column 2":[12,13,14,15,16,17,18]})
st.title("Hi! I am a Streamlit app.")
st.subheader("I am a subheader.")
st.header("I am a header.")
st.text("I am a text.")
st.markdown("[Google](https://www.google.com)")
st.latex(r"\int_a^b f(x) dx")
st.markdown("---")
st.latex(r"begin{pmatrix}a&b\\c&d\end{pmatrix}")
json={"key":"value"}
json1={"a":"1,2,3","b":2}
st.json(json1)
code="""
print("Hello World")
def funct():
    return 0;"""
st.code(code,language="python")
st.write("## H2")
st.metric(label="Wind Speed", value="120ms", delta="10ms")
st.table(tabel)
st.dataframe(tabel)