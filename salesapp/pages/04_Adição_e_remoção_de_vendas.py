from pathlib import Path
import streamlit as st
import pandas as pd
import ast
from datetime import datetime

from utilidades import leitura_dados

leitura_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']


df_filiais['cidade/estado'] = df_filiais['cidade'] + '/' + df_filiais['estado']
cidades_filiais = df_filiais['cidade/estado'].to_list()
st.sidebar.markdown('### Adição de vendas')
filial_selecionada = st.sidebar.selectbox('Selecione a filial:',
                                        cidades_filiais)

vendedores = ast.literal_eval(df_filiais.loc[df_filiais['cidade/estado'] == filial_selecionada, 'vendedores'].iloc[0])
#vendedores = vendedores.strip('][').replace("'", '').split(', ')
vendedor_selecionado = st.sidebar.selectbox('Selecione o vendedor: ', 
                                            vendedores)
produtos = df_produtos['nome'].to_list()
produto_selecionado = st.sidebar.selectbox('Selecione o produto:',
                                          produtos)

nome_cliente = st.sidebar.text_input('Nome do cliente: ')

genero_cliente = df_vendas['cliente_genero'].unique()
genero_selecionado = st.sidebar.selectbox('Selecione o gênero:',
                                          genero_cliente)

forma_pagamento = df_vendas['forma_pagamento'].unique()
forma_pagamento_selecionada = st.sidebar.selectbox('Selecione a forma de pagamento:',
                                                   forma_pagamento)

adicionar_venda = st.sidebar.button('Adicionar nova venda:')
if adicionar_venda:
    lista_adicionar = [df_vendas['id_venda'].max() + 1,
                       filial_selecionada.split('/')[0],
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero_selecionado,
                       forma_pagamento_selecionada]
    hora_adicionar = datetime.now()
    caminho_dataset = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_dataset / 'vendas.csv', decimal = ',', sep = ';')
    df_vendas.loc[hora_adicionar] = lista_adicionar
    st.dataframe(df_vendas)

st.sidebar.markdown('### Remoçãp de venda')
id_removido = st.sidebar.number_input('Selecione o ID', 
                                      0,
                                      df_vendas['id_venda'].max())
remover_venda = st.sidebar.button('Remover venda')
if remover_venda:
    df_vendas = df_vendas[df_vendas['id_venda'] != id_removido]
    caminho_dataset = st.session_state['caminho_datasets']
    df_vendas.to_csv(caminho_dataset / 'vendas.csv', decimal = ',', sep = ';')
    st.session_state['dados']['df_vendas'] = df_vendas
st.dataframe(df_vendas, height = 800)    



