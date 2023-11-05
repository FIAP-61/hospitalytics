# Libs
import pandas as pd
import streamlit as st

# Dataviz
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.header("Titulo")

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(["Distribuição Grupos de Risco", "Plano de Saúde", "Atendimento"])

# Dados
if 'df_data' not in st.session_state:
    st.session_state.df_data = pd.read_csv("pnad_covid.csv", sep=",")


with tab0:

    col1, col2, col3 = st.columns(3)
    df_risk_grouped = st.session_state.df_data.groupby(['mes_pesquisa', 'risk_group']).size().reset_index(name='contagem')
    df_month_count = st.session_state.df_data.groupby(['mes_pesquisa']).size().reset_index(name='contagem')

    with col1:
        risk_group = df_risk_grouped[df_risk_grouped['risk_group'] == 1]['contagem'].mean()
        percentage = (risk_group / df_month_count['contagem'].mean()) * 100
        st.metric(label="Qtd Média de Pessoas em Grupo de Risco durante os meses", value=f'{risk_group:.0f}', delta_color="off", delta=f'{percentage:.2f}%')

    with col2:
        df_risk_group_60 = st.session_state.df_data[(st.session_state.df_data['idade_morador'] >= 60) & (st.session_state.df_data['risk_group'] == 1)]
        risk_group_60 = df_risk_group_60.groupby(['mes_pesquisa']).size().reset_index(name='contagem')['contagem'].mean()
        percentage_60 = (risk_group_60 / df_month_count['contagem'].mean()) * 100
        st.metric(label="Qtd Média de Pessoas em Grupo de Risco com mais de 60 anos", value=f'{risk_group_60:.0f}', delta_color="off", delta=f'{percentage_60:.2f}%')

    with col3:
        st.metric(label="Qtd Média de Pessoas em Grupo de Risco com mais de 60 anos", value=f'{risk_group-risk_group_60:.0f}', delta_color="off", delta=f'{percentage-percentage_60:.2f}%')

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        # Histograma
        # fig = px.histogram(st.session_state.df_data, x="risk_group", color="sexo", barmode='group')
        # fig.update_layout(
        #     title_text='Distribuição de Grupos de Risco por Sexo',
        #     xaxis_title_text='Grupo de Risco',
        #     yaxis_title_text='Contagem',
        #     bargap=0.2,
        #     bargroupgap=0.1
        # )
        # # Atualiza as cores e a legenda
        # cores = {'1': '#3636DD', '2': '#282882'}
        # fig.for_each_trace(lambda trace: trace.update(marker=dict(color=cores[trace.name])))
        # fig.for_each_trace(lambda trace: trace.update(name = 'Masculino' if trace.name == '1' else 'Feminino'))
        # fig.update_xaxes(tickvals=[0, 1], ticktext=['Não', 'Sim'])
        # st.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(st.session_state.df_data, x="risk_group", color="sexo", facet_col="mes_pesquisa", barmode='group')
        fig.update_layout(
            title_text='Distribuição de Grupos de Risco por Sexo',
            # xaxis_title_text='',
            yaxis_title_text='Contagem',
            bargap=0.2,
            bargroupgap=0.1
        )
        cores = {'1': '#3636DD', '2': '#282882'}
        fig.for_each_trace(lambda trace: trace.update(marker=dict(color=cores[trace.name])))
        fig.for_each_trace(lambda trace: trace.update(name = 'Masculino' if trace.name == '1' else 'Feminino'))
        fig.update_xaxes(tickvals=[0, 1], ticktext=['Não', 'Sim'])
        fig.layout.annotations[0]['text'] = f'Setembro'
        fig.layout.annotations[1]['text'] = f'Outubro'
        fig.layout.annotations[2]['text'] = f'Novembro'
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown("""Texto explicando categorização do grupo de risco...""")


with tab1:

    col1, col2 = st.columns(2)

    df_grouped = st.session_state.df_data.groupby(['mes_pesquisa', 'possui_plano_saude']).size().reset_index(name='contagem')
    df_month_count = st.session_state.df_data.groupby(['mes_pesquisa']).size().reset_index(name='contagem')
    df_month_count['contagem'].mean()
    
    with col1:
        health_insurance_mean = df_grouped[df_grouped['possui_plano_saude'] == 1]['contagem'].mean()
        percentage = (health_insurance_mean / df_month_count['contagem'].mean()) * 100
        st.metric(label="Média de Pessoas com Plano de Saúde nos últimos 3 meses", value=f'{health_insurance_mean:.0f}', delta_color="off", delta=f'{percentage:.2f}%')

    with col2:
        not_health_insurance_mean =  df_month_count['contagem'].mean() - health_insurance_mean
        percentage_60 = (not_health_insurance_mean / df_month_count['contagem'].mean()) * 100
        st.metric(label="Média de Pessoas Sem Plano de Saúde nos últimos 3 meses", value=f'{not_health_insurance_mean:.0f}', delta_color="off", delta=f'{percentage_60:.2f}%')
    
    st.divider()
        
    col1, col2 = st.columns(2)

    with col1:
        df_grouped = st.session_state.df_data.groupby(['mes_pesquisa', 'possui_plano_saude']).size().reset_index(name='contagem')

        # Separando os dados para pessoas com e sem convênio
        df_com_convenio = df_grouped[df_grouped['possui_plano_saude'] == 1]
        df_sem_convenio = df_grouped[df_grouped['possui_plano_saude'] != 1]

        # Criando o gráfico de barras agrupadas
        fig = go.Figure(data=[
            go.Bar(name='Com plano de saúde', y=df_com_convenio['mes_pesquisa'], x=df_com_convenio['contagem'], orientation='h'),
            go.Bar(name='Sem plano de saúde', y=df_sem_convenio['mes_pesquisa'], x=df_sem_convenio['contagem'], orientation='h')
        ])
        fig.update_yaxes(tickvals=[9, 10, 11], ticktext=['Setembro', 'Outubro', 'Novembro'])
        fig.update_layout(barmode='group', title='Contagem de Pessoas Com e Sem Plano de Saúde ao Longo dos 3 Meses')
        st.plotly_chart(fig, use_container_width=True)

        
        with col2:
           st.markdown("""Texto explicando ...""")
    

with tab2:
    col1, col2= st.columns(2)
    
    with col1:
        total = st.session_state.df_data[['buscou_atendimento_hospital_sus', 'buscou_atendimento_ps_sus_upa', 'buscou_atendimento_posto_ubs_esf']]
        total = total[total == 1].sum().sum()
        percentage = (total / st.session_state.df_data.shape[0]) * 100
        st.metric(label="Total de Pessoas que Buscaram Atendimento em 3 Meses", value=f'{total:.0f}', delta_color="off", delta=f'{percentage:.2f}%')

    with col2:
        st.markdown(
            """
            Legenda:  
            UBS - ESF: Posto de saúde | Unidade básica de saúde | Equipe de Saúde da Família  
            PS (SUS, UPA): Pronto Socorro do SUS/UPA  
            SUS: Hospital do SUS
            """
        )

    fig = make_subplots(rows=1, cols=3)
    fig.update_layout(
            title_text='Distribuição dos Locais de Atendimento mais Procurados por Mês',
            # xaxis_title_text='',
            # yaxis_title_text='Contagem',
            # bargap=0.2,
            # bargroupgap=0.1
        )

    months = ['', 'Setembro', 'Outubro', 'Novembro']
    for i, mes in enumerate(st.session_state.df_data['mes_pesquisa'].unique(), start=1):
        soma_dados =  st.session_state.df_data[st.session_state.df_data['mes_pesquisa'] == mes][['buscou_atendimento_posto_ubs_esf', 'buscou_atendimento_ps_sus_upa', 'buscou_atendimento_hospital_sus']][st.session_state.df_data == 1].sum()
        fig.add_trace(go.Bar(x=soma_dados.index, y=soma_dados.values, name=f'{months[i]}'), row=1, col=i)
        fig.update_xaxes(tickvals=['buscou_atendimento_posto_ubs_esf', 'buscou_atendimento_ps_sus_upa', 'buscou_atendimento_hospital_sus'], ticktext=['UBS - ESF', 'PS (SUS, UPA)', 'SUS'])
    st.plotly_chart(fig, use_container_width=True)

    col1, col2= st.columns(2)
    with col1:
        stayed_home = st.session_state.df_data[st.session_state.df_data['ficou_em_casa'] == 1]['risk_group'].value_counts()
        stayed_home_title = ['Não é de Grupo de Risco', 'É do Grupo de Risco']

        fig = px.pie(values=stayed_home, names=stayed_home_title, hole=.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(title_text="Pessoas que tiveram sintomas mas permaneceram em casa")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        auto_medication = st.session_state.df_data[st.session_state.df_data['auto_medicacao'] == 1]['risk_group'].value_counts()
        auto_medication_title = ['Não é de Grupo de Risco', 'É do Grupo de Risco']

        fig = px.pie(values=auto_medication, names=auto_medication_title, hole=.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(title_text="Pessoas que tiveram sintomas e se auto medicaram")
        st.plotly_chart(fig, use_container_width=True)