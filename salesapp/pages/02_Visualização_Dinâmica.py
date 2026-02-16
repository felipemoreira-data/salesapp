from pathlib import Path
import streamlit as st
import pandas as pd

from utilidades import leitura_dados, COMISSAO

COLUNAS_ANALISE = ['filial', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
COLUNAS_VALOR = ['preco', 'comissao']
FUNCOES_AGG = {'soma': 'sum', 'contagem': 'count'}
leitura_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

df_produtos = df_produtos.rename(columns = {"nome": "produto"})
df_vendas  = df_vendas.reset_index()
df_vendas = pd.merge(left= df_vendas,
                       right=df_produtos[['produto', 'preco']],
                       on = 'produto',
                       how = 'left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

indices_selecionados = st.sidebar.multiselect('Selecione o índice',
                                             COLUNAS_ANALISE)
indice_exclusao = [c for c in COLUNAS_ANALISE if not c in indices_selecionados]
colunas_selecionadas = st.sidebar.multiselect('Selecione a coluna',
                                             indice_exclusao)
valor_analise_selecionada  = st.sidebar.selectbox('Selecione o valor da análise',
                                              COLUNAS_VALOR)

metrica_analise_selecionada  = st.sidebar.selectbox('Selecione a métrica análisada',
                                              list(FUNCOES_AGG.keys()))

if len(indices_selecionados) > 0 and len(colunas_selecionadas) > 0:
    metrica_analise_selecionada = FUNCOES_AGG[metrica_analise_selecionada]
    vendas_pivotadas = pd.pivot_table(df_vendas,
                                      index = indices_selecionados,
                                      columns= colunas_selecionadas,
                                      values = valor_analise_selecionada,
                                      aggfunc= metrica_analise_selecionada)
    vendas_pivotadas['SOMA TOTAL'] = vendas_pivotadas.sum(axis = 1)
    vendas_pivotadas.loc['SOMA TOTAL'] = vendas_pivotadas.sum(axis = 0).to_list()
    st.dataframe(vendas_pivotadas)