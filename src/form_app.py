import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Cadastro de Base de Dados das Ovitrampas")
st.markdown("Adicione os dados de referência para o mês da campanha abaixo.")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="test", usecols=list(range(11)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

SEMANA = [
    "Electronics",
    "Apparel",
    "Groceries",
    "Software",
    "Other",
]
DISTRITO = [
    "DAGUA",
    "DABEL",
    "DASAC",
    "DAENT",
    "DABEN",
    "DAICO",
    "DAOUT",
    "DAMOS"
]

# Onboarding New Vendor Form
with st.form(key="test"):
    ano = st.text_input(label="Ano*")
    mes = st.selectbox("Mês*", options=MESES, index=None)
    semana = st.selectbox("Semana*", options=SEMANA)
    distrito = st.selectbox("Distrito*", options=DISTRITO)
    cod_bairro = st.number_input(label="Código do bairro", format="%.Of")
    bairro = st.text_input(label="Bairro")
    zona = st.number_input(label="Zona", format="%.Of")
    quarteirao = st.number_input(label="Código do Quarteirão", format="%.Of")
    satelite = st.number_input(label="Código do Satélite", format="%.Of")
    nu_ovos = st.number_input("Quantidade de Ovos", format="%.Of")
    obs = st.text_area(label="Observação")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Enviar")

    # Create a new row of vendor data
    bd_siovi = pd.DataFrame(
          [
                {
                      "ano": ano,
                      "BusinessType": mes,
                      "Products": semana,
                      "YearsInBusiness": distrito,
                      "OnboardingDate": cod_bairro,
                      "AdditionalInfo": bairro,
                        "YearsInBusiness": zona,
                        "OnboardingDate": quarteirao,
                        "AdditionalInfo": satelite,
                        "YearsInBusiness": nu_ovos,
                        "OnboardingDate": obs,
                    }
                ]
            )

    # Add the new vendor data to the existing data
    updated_df = pd.concat([existing_data, bd_siovi], ignore_index=True)

    # Update Google Sheets with the new vendor data
    conn.update(worksheet="test", data=updated_df)

    st.success("Cadastro efetuado com sucesso!")
