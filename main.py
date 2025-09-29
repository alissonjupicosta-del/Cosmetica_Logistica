import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata
import openpyxl



colunas = ['Data','Pedido','NF', 'TV', 'Car','Pos','Cod','Cliente','Cidade','Praca','RCA','Vlr Atendido', 'Peso Total']

def remove_acentos(txt):
    return unicodedata.normalize('NFKD',str(txt))\
                        .encode('ASCII','ignore')\
                        .decode('utf-8')
@st.cache_data(ttl=300)
def carregar_dados():
    colunas = ['Data','Pedido','NF', 'TV', 'Car','Pos','Cod','Cliente','Cidade','Praca','RCA','Vlr Atendido', 'Peso Total']
    df = pd.read_csv('vendas.TXT',index_col=False)
    df_regiao = pd.read_excel('municipios_alagoas.xlsx')
    df.columns = colunas
    df['Data'] = pd.to_datetime(df['Data'],dayfirst=True)
    df['Vlr Atendido'] = df['Vlr Atendido'].astype(str)\
                        .str.replace('R$','',regex=False)\
                        .str.replace('.','',regex=False)\
                        .str.replace(',','.',regex=False)\
                        .str.strip()
    df['Vlr Atendido']=pd.to_numeric(df['Vlr Atendido'])
    df['Peso Total']= df['Peso Total'].str.replace('.','',regex=False)\
                        .str.replace(',','.',regex=False)\
                        .str.strip()
    df['Peso Total'] = pd.to_numeric(df['Peso Total'])
    df['Cidade']=df['Cidade'].apply(remove_acentos).str.upper()
    df['Car'] = pd.to_numeric(df['Car'])

    #Tratamento das DF_regiao
    df_regiao['Município'] = df_regiao['Município'].apply(remove_acentos).str.upper()

    #Criando DF_Final - juntando os 2

    df_final = pd.merge(df,df_regiao,left_on='Cidade',right_on='Município',how='left')
    df_final['Região'] = df_final['Região'].str.upper()
    df_final = df_final.dropna(subset=['Região'])
    return df_final

#Streamlit -- Criando os Dashboards

st.set_page_config('Dashboards - Cosmética',layout='wide')

st.title('Acompanhamento - Logística',anchor='center')


#Filtro _ carregamento

df_final = carregar_dados()

col1,col2 = st.columns(2)

with col1:
    min_data = df_final['Data'].min()
    max_data = df_final['Data'].max()

    data_selecao = st.date_input('Selecione uma data:',value=(min_data,max_data),min_value=min_data,max_value=max_data,format='DD/MM/YYYY')

with col2:
    carregamento = sorted(df_final['Car'].astype(int).unique())
    carreg_selecao = st.multiselect('Selecione o carregamento',carregamento,default=carregamento)
    

regiao = df_final['Região'].unique()
regiao_sele = st.multiselect('Selecione uma região:',regiao,default=regiao)

start_date,end_date = data_selecao

df_filtrada = df_final[(df_final['Car'].isin(carreg_selecao)) 
                       & (df_final['Região'].isin(regiao_sele))
                       &(df_final['Data']>=pd.to_datetime(start_date))&
                       (df_final['Data']<=pd.to_datetime(end_date))
                       ]

card1,card2 = st.columns(2)

with card1:
    st.metric('Valor Total:',value=f"R$ {df_filtrada['Vlr Atendido'].sum():,.2f}")

with card2:
    st.metric('🚚Qtde Entregas:',value=len(df_filtrada))

graf1,graf2 = st.columns(2)

fig_icicle = px.icicle(df_filtrada, 
                path=['Região','Cidade','Cliente'], 
                values='Vlr Atendido',title='Divisão - Região / Cidade / Cliente')

with graf1:
    df_filtrada['Pedido'] = 1
    df_agrupada = df_filtrada.groupby('Região')[['Vlr Atendido','Pedido']].sum()
    st.dataframe(df_agrupada)

with graf2:
 graf_linha = px.bar(df_filtrada.groupby('Região')['Vlr Atendido'].sum().reset_index(),x='Região',y='Vlr Atendido')
 st.plotly_chart(fig_icicle,use_container_width=True)


graf_sun = px.sunburst(df_filtrada,names='Região',path=['Região','Cidade','Cliente'],values='Vlr Atendido',title='Divisão - Região / Cidade / Cliente')

st.markdown('----------')

#st.plotly_chart(graf_sun,use_container_width=True)

fig = px.treemap(df_filtrada, 
                 path=['Região','Cidade','Cliente'], 
                 values='Vlr Atendido',
                 color='Vlr Atendido',
                 color_continuous_scale='Blues')

st.plotly_chart(fig,use_container_width=True)

fig_icicle = px.icicle(df_filtrada, 
                path=['Região','Cidade','Cliente'], 
                values='Vlr Atendido',title='Divisão - Região / Cidade / Cliente')

#st.plotly_chart(fig_icicle,use_container_width=True)

