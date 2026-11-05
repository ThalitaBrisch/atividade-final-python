import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl

st.title("📊 Dashboard de Crescimento Demográfico e Planejamento Urbano")
st.markdown("""
Bem-vindo ao **Dashboard de Crescimento Demográfico**, uma ferramenta desenvolvida para ajudar os prefeitos das capitais brasileiras a entenderem as mudanças populacionais em suas cidades.
""")

caminho = "CD2022_Populacao_2010_Compatibilizada_20231222.xlsx"

df = pd.read_excel(
    caminho,
    sheet_name="Municípios",
    skiprows=2
)

df = df.iloc[:, 1:]

df.columns = [
    "UF",
    "COD. UF",
    "COD. MUNIC",
    "NOME DO MUNICÍPIO",
    "População Município 2010",
    "População 2010 Compatibilizada",
    "População Censo 2022"
]

col_2010 = "População 2010 Compatibilizada"
col_2022 = "População Censo 2022"

filtro = ["Porto Alegre", "Belo Horizonte", "Curitiba", "Salvador", "Florianópolis"]

df_filtrado = df[df["NOME DO MUNICÍPIO"].isin(filtro)]

pop = (
    df_filtrado.groupby(["NOME DO MUNICÍPIO"], as_index=False)
      .agg(
          populacao_2010=(col_2010, "sum"),
          populacao_2022=(col_2022, "sum"),
      )
)
top = pop.melt(
    id_vars="NOME DO MUNICÍPIO",
    value_vars=["populacao_2010", "populacao_2022"],
    var_name="ano",
    value_name="populacao"
)

# Calculando os KPIs
df["Taxa de Crescimento (%)"] = ((df[col_2022] - df[col_2010]) / df[col_2010]) * 100
populacao_total_2010 = df[col_2010].sum()
populacao_total_2022 = df[col_2022].sum()
taxa_crescimento_total = ((populacao_total_2022 - populacao_total_2010) / populacao_total_2010) * 100

# Exibindo os KPIs gerais
st.markdown("## 📈 Indicadores-Chave de Desempenho (KPIs)")
st.metric(label="Taxa de Crescimento Populacional Total (%)", value=f"{taxa_crescimento_total:.2f}%")
st.metric(label="População Total (2010)", value=f"{populacao_total_2010:,}".replace(",", "."))
st.metric(label="População Total (2022)", value=f"{populacao_total_2022:,}".replace(",", "."))

fig = px.line(
    top, x='NOME DO MUNICÍPIO', y='populacao', color='ano',
    markers=True,
    line_shape='linear',
    title="PROJEÇÃO POPULACIONAL",
    color_discrete_sequence=["#FFB6C1", "#FF00FF"]
)



st.plotly_chart(fig, use_container_width=True)

st.dataframe(top)

st.markdown("---")

st.markdown("""
## 📰 Envelhecimento populacional
As amostras evidenciam uma tendência de **envelhecimento populacional** no país. Entre o grupo, ainda se percebe uma **predominância feminina**.  
> "A razão de sexo calculada para a população de 65 anos ou mais de idade indicou que existem, aproximadamente, 75,9 homens para cada 100 mulheres", aponta a pesquisa.

No entanto, não foi somente o número de idosos que cresceu. A população de **30 a 59 anos** também aumentou, atingindo **58,6% do total de habitantes em 2025**, número que superou os **50,1% registrados em 2012**.

Assim, a faixa etária dos **30 aos 60 anos** ocupa a maior entre os recortes de idade no país.

📖 [Leia mais na CNN Brasil](https://www.cnnbrasil.com.br/nacional/brasil/populacao-jovem-cai-e-numero-de-idosos-aumenta-no-brasil-aponta-ibge/)
""")

st.image(
    "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2024/07/expectativa-de-vida-medicamento.jpg?w=1200&h=900&crop=0&quality=90",
    caption="Expectativa de vida e envelhecimento populacional no Brasil"
)

st.markdown("---")

st.markdown("""
## 🏠 Queda na média de moradores por domicílio
Após a divulgação do **Censo 2022**, é possível apontar que a queda da média de moradores por domicílio registrada é fruto da **“transição demográfica”** pela qual o Brasil passa.  
É o que explica o professor da UFMG e membro da Comissão Consultiva do Censo 2022:

> “Essa transição é caracterizada pela redução da natalidade e mortalidade”, disse, à CNN Rádio.

De acordo com o demógrafo, “está em processo um grande processo de **envelhecimento da população**, com idosos com autonomia de saúde e financeira.  
Eles vivem em domicílios menores ou só com o cônjuge, então o número de pessoas por domicílio neste grupo etário diminui.”

### Outras causas:
- Redução do número de filhos
- Separação de casais

> “Temos essas várias tendências demográficas diferentes que apontam para essa queda de moradores por habitação.”

Ao mesmo tempo, o professor aponta que o envelhecimento da população vai continuar acontecendo e, com ela, virão desdobramentos:

- Populações dos municípios vão começar a **decrescer até antes de 2040**, com cidades diminuindo de tamanho.
- Consequências para a oferta de serviços e transferência de recursos para os municípios.
- Impactos na previdência e serviços de saúde.

📖 [Leia mais na CNN Brasil](https://www.cnnbrasil.com.br/nacional/brasil-vive-transicao-demografica-que-impactara-politicas-publicas-diz-professor/)
""")

st.image(
    "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/06/sp_governo_cidade_vista_aerea_270320193512.jpg?w=1200&h=900&crop=0&quality=90",
    caption="Impactos da transição demográfica nas cidades brasileiras"
)