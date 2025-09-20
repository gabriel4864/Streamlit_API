import streamlit as st
import pandas as pd
# pip install plotly
import plotly.express as px
# pip install streamlit-option-menu
from streamlit_option_menu import option_menu #para
from query import conexao # Consulta no banco de dados


# ********** Primeira consulta e atualização **********
# Consulta
query = "SELECT * FROM tb_carro"
df = conexao(query)

# Atualização
if st.button("Atualizar dados"):
    df = conexao(query)
# ****************************************

# Estrutura de filtro lateral
marca = st.sidebar.multiselect("Marca Selecionada",
                       options = df["marca"].unique(),
                       default=df["marca"].unique()
                       )

modelo = st.sidebar.multiselect("Modelo Selecionado",
                       options = df["modelo"].unique(),
                       default=df["modelo"].unique()
                       )

ano = st.sidebar.multiselect("Ano Selecionado",
                       options = df["ano"].unique(),
                       default=df["ano"].unique()
                       )

valor = st.sidebar.multiselect("Valor Selecionado",
                       options = df["valor"].unique(),
                       default=df["valor"].unique()
                       )

cor = st.sidebar.multiselect("Cor Selecionada",
                       options = df["cor"].unique(),
                       default=df["cor"].unique()
                       )

numero_Vendas = st.sidebar.multiselect("numero_Vendas Selecionado",
                       options = df["numero_Vendas"].unique(),
                       default=df["numero_Vendas"].unique()
                       )

min_vendas = int(df["numero_Vendas"].min())
max_vendas = int(df["numero_Vendas"].max())

vendas = st.sidebar.slider("Intervalo de Número de Vendas Selecionado",
                           min_value= min_vendas,
                           max_value=max_vendas,
                           value = (min_vendas, max_vendas) # Valor inicial
                           )


# *************** Verificação da aplicação dos filtros
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_Vendas"] >= vendas[0]) & 
    (df["numero_Vendas"] <= vendas[1]) 
]



# ******************* DASHBOARD ****************~
# CARDS DE VALORES
def PáginaInicial():
    # Expande para selecionar as opções 
    with st.expander("Tabela de Carros"):
        exibicao = st.multiselect("Filtro",
                                  df_selecionado.columns,
                                  default = [],
                                  key = "Filtro_Exibicao"     
                                  )
        if exibicao:
            st.write(df_selecionado[exibicao])

    
    if not df_selecionado.empty:
        total_vendas = df_selecionado["numero_Vendas"].sum()
        media_valor = df_selecionado["valor"].mean()
        media_vendas = df_selecionado["numero_Vendas"].mean() 

        card1, card2, card3 = st.columns(3, gap= "large")
        with card1:
            st.info("Valor Total de Vendas", icon= "🚗")
            st.metric(label="Total", value= f"{total_vendas:,.0f}")

        with card2:
            st.info("Valor Médio dos Carros", icon= "📈")
            st.metric(label="Média", value= f"{total_vendas:,.0f}")
        
        with card3:
            st.info("Valor Médio de Vendas", icon= "📊")
            st.metric(label="Média", value= f"{total_vendas:,.0f}")

    else:
        st.warning("Nnehum dado disponível com os filtros selecionados")
    st.markdown("""-------""")



# ******************** GRAFICOS ****************

def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("Nenhum dado disponível para gerar os gráficos")
        return

    graf1, graf2, graf3, graf4 = st.tabs(["Grafico de Barras",
                                          "Grafico de Linhas", 
                                          "Grafico de Pizza", 
                                          "Grafico de Dispersão"])

    with graf1:
        st.write("Gráfico de Barras")
        valor = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by= "valor", ascending=True)

        fig1 = px.bar(
            valor,
            x= valor.index,
            y= "valor",
            orientation="h",
            title = "Valores dos Carros",
            color_discrete_sequence=["#29A1C2"]
        )

    st.plotly_chart(fig1, use_container_width = True) # Exibição do gráfico
    

    with graf2:
        st.write("Gráfico de linhas")
        valor_linhas = df_selecionado.groupby("modelo").count()[["valor"]]

        fig2 = px.line(
            valor_linhas,
            x= valor_linhas.index,
            y= "valor",
            title = "Valor por Modelo",
            color_discrete_sequence= ["#29A1C2"]
        )
    st.plotly_chart(fig2, use_container_width = True) # Exibição do gráfico




PáginaInicial()
graficos(df_selecionado)