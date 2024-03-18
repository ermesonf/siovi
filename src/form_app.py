from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date
import yaml
from yaml.loader import SafeLoader

# --- USER AUTHENTICATION ---
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")

if st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")

if st.session_state["authentication_status"]:
    authenticator.logout()
    # Display Title and Description
    st.title("Cadastro de Base de Dados das Ovitrampas")
    st.markdown("Adicione os dados de referência para o mês da campanha abaixo.")

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read(worksheet="test", usecols=list(range(11)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    # List of Business Types and Products
    # Ler o arquivo CSV em um DataFrame
    df_bairro = pd.read_csv("./data/bairros.csv")

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

    SEMANA = list(range(1, 54))

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

    BAIRROS = df_bairro['bairro'].unique()

    INTERCORRENCIAS = [
        "Extravio",
        "Excluída",
        "Casa fechada",
        "Outros (especificar)"
    ]
    # Onboarding New Vendor Form
    with st.form(key="test"):
        ano = st.number_input("Digite o Ano", min_value=2020, max_value=date.today().year, step=1)
        mes = st.selectbox("Escolha o Mês*", options=MESES, index=None)
        semana = st.selectbox("Escolha a Semana*", options=SEMANA)
        distrito = st.selectbox("Escolha o Distrito*", options=DISTRITO)
        cod_bairro = st.number_input(label="Digite o Código do bairro", step=1)
        bairro = st.selectbox("Escolha o Bairro", options=BAIRROS)
        #bairro = st.text_input(label="Bairro")
        zona = st.number_input(label="Digite a Zona", step=1)
        quarteirao = st.number_input(label="Digite o Código do Quarteirão", step=1)
        satelite = st.number_input(label="Digite o Código do Satélite", step=1)
        nu_ovos = st.number_input("Digite a Quantidade de Ovos", step=1)
        intercorrencia = st.selectbox(label="Escolha a Intercorrência", options=INTERCORRENCIAS)
        obs = st.text_input(label="Observações")

        # Mark mandatory fields
        st.markdown("**Obrigatório*")

        submit_button = st.form_submit_button(label="Enviar")

        if submit_button:
            # Create a new row of vendor data
            bd_siovi = pd.DataFrame(
            [
                    {
                        "ANO": ano,
                        "MES": mes,
                        "SEMANA": semana,
                        "DISTRITO": distrito,
                        "COD_BAIRRO": cod_bairro,
                        "BAIRRO": bairro,
                        "ZONA": zona,
                        "COD_QT": quarteirao,
                        "COD_SATELITE": satelite,
                        "NU_OVOS": nu_ovos,
                        "INTERCOR": intercorrencia,
                        "OBS": obs
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, bd_siovi], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="test", data=updated_df)

            st.success("Cadastro efetuado com sucesso!")
