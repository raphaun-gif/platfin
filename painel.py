import streamlit as st
import yfinance as yf
import sqlite3
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Inteligência Financeira", page_icon="📈", layout="wide")
st.title("📈 Painel de Estratégia Macro")
st.write("Sua plataforma de análise de mercado gerada por Inteligência Artificial.")
st.divider()

# 2. SEÇÃO SUPERIOR: GRÁFICO DA BOLSA
st.subheader("Desempenho Recente do Ibovespa")
ibov = yf.Ticker("^BVSP")
historico = ibov.history(period="1mo")
st.line_chart(historico['Close'], use_container_width=True)

st.divider()

# 3. SEÇÃO INFERIOR: HISTÓRICO DE RELATÓRIOS DA IA
st.subheader("🤖 Relatórios do Estrategista Virtual")

try:
    # Tenta conectar no banco de dados e buscar os relatórios salvos
    conexao = sqlite3.connect("banco_dados.db")
    # Lê a tabela do banco usando a biblioteca Pandas para formatar bonitinho
    tabela = pd.read_sql_query("SELECT * FROM relatorios ORDER BY data DESC", conexao)
    conexao.close()
    
    if tabela.empty:
        st.info("Nenhum relatório foi gerado ainda. Execute o script de coleta.")
    else:
        # Se encontrou relatórios, cria um menu expansível para cada dia
        for index, linha in tabela.iterrows():
            with st.expander(f"Relatório de {linha['data']} (Ibov: {linha['ibovespa']} pts)"):
                st.write(linha['relatorio'])

except Exception as e:
    st.error("O banco de dados ainda não foi criado. Execute o script 'coleta.py' primeiro.")