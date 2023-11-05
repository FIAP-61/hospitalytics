# Libs
import pandas as pd
import streamlit as st

# Dataviz
import plotly.express as px
import plotly.graph_objects as go


# Dados
df = pd.read_csv(r".\Source\pnad_covid.csv", sep=",")
uf_dict = {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima', 15: 'Pará', 16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão', 22: 'Piauí', 23: 'Ceará', 24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco', 27: 'Alagoas', 28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo', 33: 'Rio de Janeiro', 35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina', 43: 'Rio Grande do Sul', 50: 'Mato Grosso do Sul', 51: 'Mato Grosso', 52: 'Goiás', 53: 'Distrito Federal'}
df['uf'] = df['uf'].replace(uf_dict)

st.header("Análise Geral do Comportamento da base de dados")

# Layout do aplicativo
tab0, tab1 = st.tabs(["Análise de Respostas", "Análise da Idade"])

# Separando as Tabs
with tab0:
    
    man = df.loc[df["sexo"] == 1].shape[0]
    women = df.loc[df["sexo"] == 2].shape[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Quantidade de Respostas", value=df.shape[0], delta="")

    with col2:
        st.metric(label="N° Mulheres", value=women)

    with col3:
        st.metric(label="N° Homens", value=man)


    # Gráfico de Barras
    counts = df['uf'].value_counts().reset_index()
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


    # col1, col2 = st.columns(2)

    # with col1:
    #     # Gráfico de pizza
    #     valores = [man, women]
    #     labels = ["Homens", "Mulheres"]

    #     fig = go.Figure(
    #         data=[
    #             go.Pie(
    #                 labels=labels,
    #                 values=valores,
    #                 hole=0.3,
    #                 marker=dict(colors=["#454568", "#3636DD"]),
    #             )
    #         ]
    #     )

    #     st.subheader("Diferença do Sexo")
    #     st.plotly_chart(fig, use_container_width=True)

    # Suponha que 'df' é o seu DataFrame e 'state' é a coluna com as siglas dos estados
    df['count'] = df.groupby('uf')['uf'].transform('count')



    # Número de homens
    # Número de mulheres
    # Número das pessoas que são pacientes de risco
    # Dessas pessoas quantas tem convenio médico

    # Quantos % das pessoas de risco tem convênio

    # Mapa de Risco ou mapa com quantidade de pessoas
