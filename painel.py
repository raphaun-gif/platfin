import streamlit as st
import yfinance as yf
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Inteligência Financeira", page_icon="📈", layout="wide")
st.title("📈 Painel de Estratégia Macro")
st.write("Sua plataforma de análise de mercado gerada por Inteligência Artificial.")
st.divider()

st.subheader("Desempenho Recente do Ibovespa")
ibov = yf.Ticker("^BVSP")
historico = ibov.history(period="1mo")
st.line_chart(historico['Close'], use_container_width=True)

st.divider()

st.subheader("🤖 Relatórios do Estrategista Virtual")

ID_PLANILHA = "1Meri4ls9oS2Fylls2EONiNwIMhkXQtPa5ve03kRWCuE"

try:
    escopos = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # Detecção automática: Lê o cofre da nuvem (se online) ou o arquivo JSON (se local)
    if "GOOGLE_CREDENTIALS" in st.secrets:
        creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        credenciais = Credentials.from_service_account_info(creds_dict, scopes=escopos)
    else:
        credenciais = Credentials.from_service_account_file('credenciais.json', scopes=escopos)
        
    cliente_sheets = gspread.authorize(credenciais)
    planilha = cliente_sheets.open_by_key(ID_PLANILHA)
    aba = planilha.sheet1
    
    dados = aba.get_all_records()
    tabela = pd.DataFrame(dados)
    
    if tabela.empty:
        st.info("Nenhum relatório foi gerado ainda na nuvem.")
    else:
        # Inverte para mostrar os mais recentes no topo
        tabela = tabela.iloc[::-1]
        for index, linha in tabela.iterrows():
            with st.expander(f"Relatório de {linha['data']} (Ibov: {linha['ibovespa']} pts)"):
                st.write(linha['relatorio'])

except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados em nuvem: {e}")