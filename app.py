import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración básica de la página
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Estilo de seaborn
sns.set_style("whitegrid")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = cargar_datos()

st.sidebar.header('Filtros del Dashboard')

tipo_productos = st.sidebar.multiselect(
    'Tipo de producto',
    options=[
        'Electronic accessories','Fashion accessories','Food and beverages',
        'Health and beauty','Home and lifestyle','Sports and travel'
    ],
    default=[
        'Electronic accessories','Fashion accessories','Food and beverages',
        'Health and beauty','Home and lifestyle','Sports and travel'
    ]
)

fch_ini, fch_fin = st.sidebar.slider(
    "Selecciona el rango de fechas",
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date(),
    value=(df['Date'].min().date(), df['Date'].max().date()),
    format="YYYY-MM-DD"
)

st.subheader('1.- Exploración básica de datos')

df_filtrado = df[
    (df['Product line'].isin(tipo_productos)) &
    (df['Date'].dt.date >= fch_ini) &
    (df['Date'].dt.date <= fch_fin)
]

c1_f1, c2_f1, c3_f1 = st.columns([1,1,1])

with c1_f1:
    hist = df_filtrado.groupby('Payment').count()
    hist_max = hist['Total'].idxmax()
    hist_max_valor = hist.loc[hist_max, 'Total']
    fig1, ax1 = plt.subplots()
    ax1.hist(df_filtrado['Payment'], bins=5, edgecolor='black')
    ax1.set_title('Ventas según tipo de pago')
    st.pyplot(fig1)
    st.write(f"Método más usado: **{hist_max}** con **{hist_max_valor}** ventas")

with c2_f1:
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=df_filtrado, x='Product line', y='Unit price', ax=ax2)
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_title("Distribución de precios por producto")
    st.pyplot(fig2)

with c3_f1:
    ganancias_ciudad = df_filtrado.groupby('City')['Total'].sum().reset_index()
    idx = ganancias_ciudad['Total'].idxmax()
    ciudad, valor = ganancias_ciudad.loc[idx, ['City','Total']]
    fig3, ax3 = plt.subplots()
    ax3.bar(ganancias_ciudad['City'], ganancias_ciudad['Total'])
    ax3.set_title('Total de ventas por Ciudad')
    st.pyplot(fig3)
    st.write(f"Ciudad top: **{ciudad}** con **${valor:.1f}**")
