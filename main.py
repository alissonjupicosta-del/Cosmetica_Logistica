import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title='Comercial Meta',initial_sidebar_state='auto',layout='wide')

url_dados = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTwCqOyA5ho-4TpZAKTR9WmQxTbzY8eW2NWChfykbY99r0_zvJJiqeiWdcgGY0Yug/pub?output=csv'

df= pd.read_csv(url_dados)

#TRATAMENTO DE DADOS NUMEROS
df['VLR_VENDIDO'] = (df['VLR_VENDIDO'].astype(str)
                     .str.replace('.','',regex=False)
                     .str.replace(',','.',regex=False)
                     .str.replace('R$','',regex=False)
                     )
df['VLR_VENDIDO'] = pd.to_numeric(df['VLR_VENDIDO'],errors='coerce')
df['OBJ'] = (df['OBJ'].astype(str)
                     .str.replace('.','',regex=False)
                     .str.replace(',','.',regex=False)
                     .str.replace('R$','',regex=False)
                     )
df['OBJ'] = pd.to_numeric(df['OBJ'],errors='coerce')
df['CLI_POS']=pd.to_numeric(df['CLI_POS'],errors='coerce')
df['CLI_POS'] = df['CLI_POS'].astype('Int64')
df['META'] = (df['VLR_VENDIDO']/df['OBJ'])
df['META_POS'] = (df['CLI_POS']/df['OBJ POS'])
df['RCA'] = df['RCA'].astype('Int64')

vendedores = sorted(df['VENDEDOR_x'].unique())
vend_selec = st.sidebar.multiselect('Selecione o Vendedor:',vendedores)
fornecedores = sorted(df['FORNECEDOR'].unique())
forn_selec = st.sidebar.multiselect('Selecione o fornecedor:',fornecedores)

nova_ordem = ['RCA','VENDEDOR_x','FORNECEDOR','OBJ POS','CLI_POS','META_POS','OBJ','VLR_VENDIDO','META']
df_filtrado = df.copy()

if vend_selec:
    df_filtrado=df_filtrado[df_filtrado['VENDEDOR_x'].isin(vend_selec)]

if forn_selec:
    df_filtrado=df_filtrado[df_filtrado['FORNECEDOR'].isin(forn_selec)]

df_filtrado = df_filtrado[nova_ordem]
# -------------------------------------------



st.title('💼 Acompanhamento Vendas')
st.subheader('🏹 Verificação de meta:')

st.dataframe(
    df_filtrado.style.format({
        'META':lambda x : f'{x:.1%}',
        'OBJ': lambda x : f'R$ {x:,.2f}'.replace(',','x').replace('.',',').replace('x','.'),
        'VLR_VENDIDO':lambda x : f'R$ {x:,.2f}'.replace(',','x').replace('.',',').replace('x','.'),
        'META_POS':lambda x: f'{x:.1%}',
        'RCA': lambda x : x
    })
)



