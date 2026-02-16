from pathlib import Path
import streamlit as st
import pandas as pd

from utilidades import leitura_dados
leitura_dados()


df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

def mostrar_vendas():
    st.sidebar.divider()
    st.markdown('#### Tabela Vendas     ')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_vendas.columns),
                                                  list(df_vendas.columns))
    col, col2 = st.sidebar.columns(2)
    filtro_selecionado = col.selectbox('Filtrar Coluna',
                                      list(df_vendas.columns))
    valores_unicos_col = list(df_vendas[filtro_selecionado].unique())
    filtro_colunas = col2.selectbox('Valor do filtro', 
                                    valores_unicos_col)
    filtrar = col.button('Filtrar')
    limpar = col2.button('Limpar')

    if filtrar:
        st.dataframe(df_vendas.loc[df_vendas[filtro_selecionado] == filtro_colunas, colunas_selecionadas], height =800)
    elif limpar:
        st.dataframe(df_vendas[colunas_selecionadas], height =800)
    else:
        st.dataframe(df_vendas[colunas_selecionadas], height =800)    

def mostrar_produtos():
    st.dataframe(df_produtos)
def mostrar_filiais():
    st.dataframe(df_filiais)

st.sidebar.markdown('### Seleção de Tabelas')
tabela_selecionada = st.sidebar.selectbox('Selecione a tabela que você deseja ver:',
                                          ['Vendas', 'Produtos', 'Filiais'])

if tabela_selecionada == 'Vendas':
    mostrar_vendas()

if tabela_selecionada == 'Produtos':
    mostrar_produtos()

if tabela_selecionada == 'Filiais':
    mostrar_filiais()
