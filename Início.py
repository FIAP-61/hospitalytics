import streamlit as st
import pandas as pd
# Configurações da página
st.set_page_config(page_title="Início", page_icon="🏥", layout="wide")

st.write("# Hospitalytics: Explorando os dados do PNAD Covid 🏥")

st.markdown(
    """
O FinAlytics é uma plataforma interativa de análise e modelos de dados que oferece análises preditivas sobre os dados da IBOVESPA (Bolsa de Valores). Nossa aplicação web, construída com Streamlit, reúne informações abrangentes de séries temporais e visualizações intuitivas para facilitar a compreensão e a tomada de decisões estratégicas sobre o fechamento da base.

Explore a característica dos dados e os modelos preditivos que fornecem dados sobre a evolução das cotações diárias em valores, os gráficos e outros aspectos relevantes do modelo. Navegue pelos diferentes painéis para descobrir tendências, identificar as principais variações e compreender o nível de confiança de cada simulação que melhor se aplica à análise.

Nosso objetivo é fornecer uma experiência intuitiva e rica em informações para que você possa explorar, analisar e extrair insights valiosos (assim como os nossos) do mundo dos dados do mercado da bolsa de valores.
"""
)


# Layout do aplicativo
tab0, tab1 = st.tabs(["Ferramentas Utilizadas", "Colunas Selecionadas"])


with tab0:
    st.markdown(
        """
    ## Ferramentas Utilizadas Durante o Desevolvimento
    """
    )

    st.image("Images/tools.png")

    st.markdown(
    """
    ### Base de Dados &  Transformação
    Os dados foram ingeridos dentro do sistema de DBFS (Sistema de Arquivos do Databricks).   
    Com o pyspark dentro do databricks foi possível criar a tabela final para o streamlit consumir os dados, fazendo diversos tratamentos e utilizando as bases do PNAN Covid referentes aos meses de setembro, outubro e novembro de 2020.  
    Acesse o link para visualizar o notebook.    
    [Databricks Notebook ↗](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/5375801336056031/59063656447375/8314753084412668/latest.html)
    #
    """
    )

    st.markdown(
    """
    ### Conexão com os Dados
    Por uma limitação do databricks community não é possível criar um "personal access token" para a consulta da tabela pelo streamlit, portanto utilizaremos a exportação dessa tabela para o streamlit ingerir os dados, caso contrário seria possível conectar ao databricks pelo código na imagem abaixo.
    """
    )
    with st.expander("Clique para ver o código de conexão"):
        st.image("Images/databricks_connection.png")


with tab1:
    df_chosen_cols = pd.read_csv('chosen_cols.csv', sep='	')
    st.markdown(
        """
        # Colunas Selecionadas 
        Foi realizado uma análise dentre aproximadamente 150 colunas disponíveis dentro da base do PNAD Covid, e foram selecionadas as descritas na tabela a seguir.   
        As colunas que estão numeradas em "Coluna Escolhida" são as que entram na contagem do limite de 20 colunas possíveis.  
        """
        )
    st.dataframe(df_chosen_cols)


if 'df_data' not in st.session_state:
    df1 = pd.read_csv('pnad_covid_1.csv', sep=',')
    df2 = pd.read_csv('pnad_covid_2.csv', sep=',')
    st.session_state.df_data = pd.concat([df1, df2], axis=0, ignore_index=True)
        