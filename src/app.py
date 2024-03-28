import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="test")

# Convertendo os dados para um DataFrame do Pandas
df = pd.DataFrame(data)

# Removendo as linhas e colunas vazias
df = df.dropna(how='all')

st.dataframe(df)

# teste temp