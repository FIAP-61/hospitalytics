# Libs
import pandas as pd
import streamlit as st

# Dataviz
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurações da página
st.set_page_config(page_title="Início", page_icon="🏥", layout="wide")
st.header("Insights Extraídos")

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(
    [
        "Distribuição Grupos de Risco",
        "Distribuição de Plano de Saúde",
        "Preferências de Atendimento",
    ]
)
st.subheader("Perfilando o Risco: Quem é Mais Vulnerável?")
st.markdown(
    """
A identificação dos grupos de risco é uma parte vital da gestão de pandemias. A análise dos dados indica a porcentagem da população que pertence a grupos de risco específicos, permitindo priorizar recursos e estratégias de intervenção para aqueles que mais precisam.
"""
)

st.subheader("Desigualdades em Saúde: O Conto dos Planos")
st.markdown(
    """A posse de um plano de saúde é um fator determinante na qualidade do atendimento recebido durante a pandemia. Os dados mostram que 77,33% das pessoas não possuíam plano de saúde, indicando uma forte dependência dos serviços públicos. Essas estatísticas são fundamentais para compreender como expandir e melhorar o acesso à saúde em momentos críticos."""
)

st.subheader("Preferências de Atendimento: As Escolhas Durante a Pandemia")
st.markdown(
    """Quando confrontadas com a necessidade de cuidados médicos durante a pandemia, as preferências da população fornecem insights valiosos sobre a confiança nos diferentes níveis do sistema de saúde. Os dados do PNAD-COVID-19 iluminam estas escolhas, sugerindo áreas para melhoria e adaptação em preparação para futuras crises de saúde."""
)

# Dados
if "df_data" not in st.session_state:
    df1 = pd.read_csv("pnad_covid_1.csv", sep=",")
    df2 = pd.read_csv("pnad_covid_2.csv", sep=",")
    st.session_state.df_data = pd.concat([df1, df2], axis=0, ignore_index=True)


with tab0:
    col1, col2, col3 = st.columns(3)
    df_risk_grouped = (
        st.session_state.df_data.groupby(["mes_pesquisa", "risk_group"])
        .size()
        .reset_index(name="contagem")
    )
    df_month_count = (
        st.session_state.df_data.groupby(["mes_pesquisa"])
        .size()
        .reset_index(name="contagem")
    )

    with col1:
        risk_group = df_risk_grouped[df_risk_grouped["risk_group"] == 1][
            "contagem"
        ].mean()
        percentage = (risk_group / df_month_count["contagem"].mean()) * 100
        st.metric(
            label="Qtd Média de Pessoas em Grupo de Risco durante os meses",
            value=f"{risk_group:.0f}",
            delta_color="off",
            delta=f"{percentage:.2f}%",
        )

    with col2:
        df_risk_group_60 = st.session_state.df_data[
            (st.session_state.df_data["idade_morador"] >= 60)
            & (st.session_state.df_data["risk_group"] == 1)
        ]
        risk_group_60 = (
            df_risk_group_60.groupby(["mes_pesquisa"])
            .size()
            .reset_index(name="contagem")["contagem"]
            .mean()
        )
        percentage_60 = (risk_group_60 / df_month_count["contagem"].mean()) * 100
        st.metric(
            label="Qtd Média de Pessoas em Grupo de Risco >= 60 anos",
            value=f"{risk_group_60:.0f}",
            delta_color="off",
            delta=f"{percentage_60:.2f}%",
        )

    with col3:
        st.metric(
            label="Qtd Média de Pessoas em Grupo de Risco < 60 anos",
            value=f"{risk_group-risk_group_60:.0f}",
            delta_color="off",
            delta=f"{percentage-percentage_60:.2f}%",
        )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """Texto explicando categorização do grupo de risco e o gráfico..."""
        )

    with col2:
        fig = px.histogram(
            st.session_state.df_data,
            x="risk_group",
            color="sexo",
            facet_col="mes_pesquisa",
            barmode="group",
        )
        fig.update_layout(
            title_text="Distribuição de Grupos de Risco por Sexo",
            # xaxis_title_text='',
            yaxis_title_text="Contagem",
            bargap=0.2,
            bargroupgap=0.1,
        )
        cores = {"1": "#3636DD", "2": "#282882"}
        fig.for_each_trace(
            lambda trace: trace.update(marker=dict(color=cores[trace.name]))
        )
        fig.for_each_trace(
            lambda trace: trace.update(
                name="Masculino" if trace.name == "1" else "Feminino"
            )
        )
        fig.update_xaxes(tickvals=[0, 1], ticktext=["Não", "Sim"])
        fig.layout.annotations[0]["text"] = f"Setembro"
        fig.layout.annotations[1]["text"] = f"Outubro"
        fig.layout.annotations[2]["text"] = f"Novembro"
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        stayed_home = st.session_state.df_data[
            st.session_state.df_data["ficou_em_casa"] == 1
        ]["risk_group"].value_counts()
        stayed_home_title = ["Não é de Grupo de Risco", "É do Grupo de Risco"]

        fig = px.pie(values=stayed_home, names=stayed_home_title, hole=0.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(
            title_text="Pessoas que tiveram sintomas mas permaneceram em casa"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""Texto Explicando.....""")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""Texto Explicando.....""")

    with col2:
        auto_medication = st.session_state.df_data[
            st.session_state.df_data["auto_medicacao"] == 1
        ]["risk_group"].value_counts()
        auto_medication_title = ["Não é de Grupo de Risco", "É do Grupo de Risco"]

        fig = px.pie(values=auto_medication, names=auto_medication_title, hole=0.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(title_text="Pessoas que tiveram sintomas e se auto medicaram")
        st.plotly_chart(fig, use_container_width=True)


with tab1:
    col1, col2 = st.columns(2)

    df_grouped = (
        st.session_state.df_data.groupby(["mes_pesquisa", "possui_plano_saude"])
        .size()
        .reset_index(name="contagem")
    )
    df_month_count = (
        st.session_state.df_data.groupby(["mes_pesquisa"])
        .size()
        .reset_index(name="contagem")
    )
    df_month_count["contagem"].mean()

    with col1:
        health_insurance_mean = df_grouped[df_grouped["possui_plano_saude"] == 1][
            "contagem"
        ].mean()
        percentage = (health_insurance_mean / df_month_count["contagem"].mean()) * 100
        st.metric(
            label="Média de Pessoas com Plano de Saúde nos últimos 3 meses",
            value=f"{health_insurance_mean:.0f}",
            delta_color="off",
            delta=f"{percentage:.2f}%",
        )

    with col2:
        not_health_insurance_mean = (
            df_month_count["contagem"].mean() - health_insurance_mean
        )
        percentage_60 = (
            not_health_insurance_mean / df_month_count["contagem"].mean()
        ) * 100
        st.metric(
            label="Média de Pessoas Sem Plano de Saúde nos últimos 3 meses",
            value=f"{not_health_insurance_mean:.0f}",
            delta_color="off",
            delta=f"{percentage_60:.2f}%",
        )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        df_grouped = (
            st.session_state.df_data.groupby(["mes_pesquisa", "possui_plano_saude"])
            .size()
            .reset_index(name="contagem")
        )

        # Separando os dados para pessoas com e sem convênio
        df_com_convenio = df_grouped[df_grouped["possui_plano_saude"] == 1]
        df_sem_convenio = df_grouped[df_grouped["possui_plano_saude"] != 1]

        # Criando o gráfico de barras agrupadas
        fig = go.Figure(
            data=[
                go.Bar(
                    name="Com plano de saúde",
                    y=df_com_convenio["mes_pesquisa"],
                    x=df_com_convenio["contagem"],
                    orientation="h",
                ),
                go.Bar(
                    name="Sem plano de saúde",
                    y=df_sem_convenio["mes_pesquisa"],
                    x=df_sem_convenio["contagem"],
                    orientation="h",
                ),
            ]
        )
        fig.update_yaxes(
            tickvals=[9, 10, 11], ticktext=["Setembro", "Outubro", "Novembro"]
        )
        fig.update_layout(
            barmode="group",
            title="Contagem de Pessoas Com e Sem Plano de Saúde ao Longo dos 3 Meses",
        )
        st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("""Texto explicando ...""")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""Texto explicando ...""")

    with col2:
        risk_healthcare = st.session_state.df_data[
            st.session_state.df_data["risk_group"] == 1
        ]["possui_plano_saude"].value_counts()
        risk_healthcare_title = ["Sem plano de saúde", "Com plano de saúde", "Ignorado"]

        fig = px.pie(values=risk_healthcare, names=risk_healthcare_title, hole=0.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(
            title_text="Distribuição de Plano de Saúde em Pessoas que estão no Grupo de Risco"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    df_risk_values = st.session_state.df_data[
        (st.session_state.df_data["risk_group"] == 1)
        & (st.session_state.df_data["possui_plano_saude"] == 2)
    ]
    fig = px.histogram(
        df_risk_values, x="valores_recebidos_faixa", color="risk_group", barmode="group"
    )
    fig.update_layout(bargap=0.1)
    fig.update_layout(
        title_text="Distribuição da Renda Mensal de Pessoas que não tem Plano de Saúde e é de Grupo de Risco",
        showlegend=False,
    )
    fig.update_xaxes(
        ticktext=[
            "0 - 100",
            "101 - 300",
            "301 - 600",
            "601 - 800",
            "801 - 1.600",
            "1.601 - 3.000",
            "3.001 - 10.000",
            "10.001 - 50.000",
        ],
        tickvals=["0", "1", "2", "3", "4", "6", "7"],
        title_text="Faixa de Valores Recebidos por Mês em R$)",
    )
    fig.update_yaxes(title_text="Número de Pessoas")
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    col1, col2 = st.columns(2)
    with col1:
        total = st.session_state.df_data[
            [
                "buscou_atendimento_hospital_sus",
                "buscou_atendimento_ps_sus_upa",
                "buscou_atendimento_posto_ubs_esf",
            ]
        ]
        total = total[total == 1].sum().sum()
        percentage = (total / st.session_state.df_data.shape[0]) * 100
        st.metric(
            label="Total de Pessoas que Buscaram Atendimento em 3 Meses",
            value=f"{total:.0f}",
            delta_color="off",
            delta=f"{percentage:.2f}%",
        )

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
        title_text="Distribuição dos Locais de Atendimento mais Procurados por Mês",
        # xaxis_title_text='',
        # yaxis_title_text='Contagem',
        # bargap=0.2,
        # bargroupgap=0.1
    )

    months = ["", "Setembro", "Outubro", "Novembro"]
    for i, mes in enumerate(st.session_state.df_data["mes_pesquisa"].unique(), start=1):
        soma_dados = st.session_state.df_data[
            st.session_state.df_data["mes_pesquisa"] == mes
        ][
            [
                "buscou_atendimento_posto_ubs_esf",
                "buscou_atendimento_ps_sus_upa",
                "buscou_atendimento_hospital_sus",
            ]
        ][
            st.session_state.df_data == 1
        ].sum()
        fig.add_trace(
            go.Bar(x=soma_dados.index, y=soma_dados.values, name=f"{months[i]}"),
            row=1,
            col=i,
        )
        fig.update_xaxes(
            tickvals=[
                "buscou_atendimento_posto_ubs_esf",
                "buscou_atendimento_ps_sus_upa",
                "buscou_atendimento_hospital_sus",
            ],
            ticktext=["UBS - ESF", "PS (SUS, UPA)", "SUS"],
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""Texto explicando gráfico acima...""")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        stayed_hospitalized = st.session_state.df_data[
            st.session_state.df_data["ficou_internado"] != 9
        ]["ficou_internado"].value_counts()
        stayed_hospitalized_title = [
            "Não ficou internado",
            "Ficou internado por um dia ou mais",
            "Não foi atendido",
        ]

        fig = px.pie(
            values=stayed_hospitalized, names=stayed_hospitalized_title, hole=0.3
        )
        fig.update_traces(textfont_size=20)
        fig.update_layout(title_text="Pessoas que tiveram que ser internadas")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""Texto Explicando.....""")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""Texto Explicando.....""")

    with col2:
        risk_hospitalized = st.session_state.df_data[
            st.session_state.df_data["internado_risco"] != 9
        ]["internado_risco"].value_counts()
        risk_hospitalized_title = ["Não", "Sim"]

        fig = px.pie(values=risk_hospitalized, names=risk_hospitalized_title, hole=0.3)
        fig.update_traces(textfont_size=20)
        fig.update_layout(
            title_text="Pessoas que durante a internação, foram sedadas, entubadas e colocadas em respiração artificial com ventilador"
        )
        st.plotly_chart(fig, use_container_width=True)
