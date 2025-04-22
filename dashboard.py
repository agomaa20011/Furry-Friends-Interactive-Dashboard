# Setting the environment
import streamlit as st
import pandas as pd
import plotly.express as px

# Loading data
df = pd.read_excel(r'D:/DATA SCIENCE/assigenment/Fury_Friends data set_4376.xlsx')

# Data exploration in console (can remove for production)
print(df.head())
print(df.info())
print(df.isna().sum())

# Cleaning and feature engineering
# Drop missing manager names
df = df.dropna(subset=['Managers First Name', 'Managers Surname'])
# Compute profit
df['Profit'] = df['Revenue'] - df['Cost']
# Create store identifier
df['Store'] = df['Managers First Name'] + ' ' + df['Managers Surname']
# Drop rows with any remaining nulls in key numeric columns
df = df.dropna(subset=['Units Sld', 'Revenue', 'Cost', 'Profit'])

# Title of the dashboard
st.set_page_config(page_title="Fury Friends Dashboard", layout="wide")
st.title("🐾 Fury Friends Pet Store Performance Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    area = st.multiselect("Select Area:", options=df['Area'].unique(), default=df['Area'].unique())
    pet = st.multiselect("Select Pet Type:", options=df['Pet'].unique(), default=df['Pet'].unique())
    date_range = st.date_input("Select Date Range:", [df['Date'].min(), df['Date'].max()])

# Apply filters
df_filtered = df[
    (df['Area'].isin(area)) &
    (df['Pet'].isin(pet)) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

# Layout for key metrics
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"£{df_filtered['Revenue'].sum():,.2f}")
col2.metric("Total Cost", f"£{df_filtered['Cost'].sum():,.2f}")
col3.metric("Total Profit", f"£{df_filtered['Profit'].sum():,.2f}")

# Summary statistics section
st.markdown("---")
st.subheader("📊 Summary Statistics")
# Top 5 Stores by Revenue
top_stores_rev = df_filtered.groupby('Store')['Revenue'].sum().nlargest(5).reset_index()
fig_top_rev = px.bar(top_stores_rev, x='Store', y='Revenue', title="Top 5 Stores by Revenue")
fig_top_rev.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig_top_rev, use_container_width=True)
# Top 5 Stores by Profit
top_stores_prof = df_filtered.groupby('Store')['Profit'].sum().nlargest(5).reset_index()
fig_top_prof = px.bar(top_stores_prof, x='Store', y='Profit', title="Top 5 Stores by Profit")
fig_top_prof.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig_top_prof, use_container_width=True)
# Top Areas by Revenue
top_areas = df_filtered.groupby('Area')['Revenue'].sum().nlargest(5).reset_index()
fig_area = px.bar(top_areas, x='Area', y='Revenue', title="Top 5 Areas by Revenue")
fig_area.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig_area, use_container_width=True)

# Main charts
st.markdown("---")
st.subheader("Performance Overviews")
# Profit by Store
fig1 = px.bar(df_filtered.groupby('Store')['Profit'].sum().reset_index(), x='Store', y='Profit', title="Profit by Store")
fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)
# Profit by Area
fig2 = px.bar(df_filtered.groupby('Area')['Profit'].sum().reset_index(), x='Area', y='Profit', title="Profit by Area")
fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig2, use_container_width=True)
# Profit by Pet Type
fig3 = px.bar(df_filtered.groupby('Pet')['Profit'].sum().reset_index(), x='Pet', y='Profit', title="Profit by Pet Type")
fig3.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig3, use_container_width=True)
# Revenue vs Cost Over Time
df_time = df_filtered.groupby('Date')[['Revenue', 'Cost']].sum().reset_index()
fig4 = px.line(df_time, x='Date', y=['Revenue', 'Cost'], title="Revenue vs Cost Over Time")
fig4.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig4, use_container_width=True)
# Profit Trend Over Time
df_profit_trend = df_filtered.groupby('Date')['Profit'].sum().reset_index()
fig5 = px.line(df_profit_trend, x='Date', y='Profit', title="Profit Trend Over Time")
fig5.update_layout(margin=dict(l=20, r=20, t=40, b=20), template='plotly_white')
st.plotly_chart(fig5, use_container_width=True)

# Footer or additional notes
st.markdown("---")
st.write("Data last updated:", df['Date'].max().date())
