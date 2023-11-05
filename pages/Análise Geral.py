# Libs
import pandas as pd
import streamlit as st

# Dataviz
import plotly.express as px


st.header("Análise Geral do Comportamento da base de dados")

# Layout do aplicativo
tab0, tab1 = st.tabs(["Análise de Respostas", "Análise da Idade"])

# Dados
if 'df_data' not in st.session_state:
    st.session_state.df_data = pd.read_csv("pnad_covid.csv", sep=",")

# Transform
uf_dict = {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima', 15: 'Pará', 16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão', 22: 'Piauí', 23: 'Ceará', 24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco', 27: 'Alagoas', 28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo', 33: 'Rio de Janeiro', 35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina', 43: 'Rio Grande do Sul', 50: 'Mato Grosso do Sul', 51: 'Mato Grosso', 52: 'Goiás', 53: 'Distrito Federal'}
st.session_state.df_data['uf'] = st.session_state.df_data['uf'].replace(uf_dict)


with tab0:
    
    gen_count = st.session_state.df_data['sexo'].value_counts()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Quantidade de Respostas", value=st.session_state.df_data.shape[0], delta_color="off", delta='100%')

    with col2:
        st.metric(label="N° de Mulheres", value=gen_count[2], delta_color="off", delta='52,1%')

    with col3:
        st.metric(label="N° de Homens", value=gen_count[1], delta_color="off", delta='47,9%')


    # Gráfico de Barras
    counts = st.session_state.df_data['uf'].value_counts().reset_index()
    counts.columns = ['Estado', 'Quantidade']
    fig = px.bar(counts, y='Estado', x='Quantidade', orientation='h', title='Número de Respostas por Estado', text='Quantidade')

    # Layout e cor
    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        xaxis_title="Número de Respostas",
        yaxis_title=""
    )
    fig.update_traces(marker_color='#3636DD')
    st.plotly_chart(fig, use_container_width=True)


with tab1:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Idade Média", value=round(st.session_state.df_data['idade_morador'].mean(), 2), delta_color="off", delta='100%')

    with col2:
        elders = st.session_state.df_data[st.session_state.df_data['idade_morador'] >= 60].shape[0]
        percentage = (elders / st.session_state.df_data.shape[0]) * 100
        st.metric(label="Quantidade Pessoas com mais de 60 anos", value=elders, delta_color="off", delta=f'{percentage:.2f}%')

    with col3:
        elders = st.session_state.df_data[st.session_state.df_data['idade_morador'] < 60].shape[0]
        percentage = (elders / st.session_state.df_data.shape[0]) * 100
        st.metric(label="Quantidade Pessoas com menos de 60 anos", value=elders, delta_color="off", delta=f'{percentage:.2f}%')
    
    fig = px.histogram(st.session_state.df_data, x="idade_morador")

    fig.update_layout(
        title_text='Histograma de Idades',
        xaxis_title_text='Idade', 
        yaxis_title_text='Número de Pessoas',
        bargap=0.2, 
        bargroupgap=0.1 
    )

    fig.update_traces(marker_color='#3636DD')
    st.plotly_chart(fig, use_container_width=True)

    # Número de homens
    # Número de mulheres

    # Quantidade de pessoas com os sintomas, cada sintoma um card
    # Categorizar e explicar os grupos de risco

    # Número das pessoas que são pacientes de risco
    # N de pessoas com menos de 60 anos que sao paciente de risco
    
    # Dessas pessoas quantas tem convenio médico
    # Quantos % das pessoas de risco tem convênio
    # Mapa de Risco ou mapa com quantidade de pessoas
