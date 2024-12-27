import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from datetime import datetime

sns.set(style="darkgrid")

def create_daily_report(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    daily_orders_df = df[(df['order_purchase_timestamp'] >= start_date) & (df['order_purchase_timestamp'] <= end_date)]
    return daily_orders_df

def create_product_performance(df, start_date, end_date, token):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(df['order_purchase_timestamp'] >= start_date) & (df['order_purchase_timestamp'] <= end_date)]
    if token == 'product_performance':
        product_performance_df = filtered_df.groupby('category_name_english')['total_price'].sum().sort_values(ascending=False).reset_index()
        return product_performance_df.head(10)
    elif token == 'customer_spending':
        customer_spending_df = filtered_df.groupby('customer_unique_id')['total_price'].sum().sort_values(ascending=False).reset_index()
        return customer_spending_df.head(10)
    elif token == 'customer_demographic':
        customer_demographic_df = filtered_df.groupby('customer_state')['customer_unique_id'].count().sort_values(ascending=False).reset_index()
        customer_demographic_df.rename(columns={'customer_state': 'customer_state', 'customer_unique_id': 'customer_count'}, inplace=True)
        return customer_demographic_df.head(10)
    elif token == 'product_count':
        product_count_df = filtered_df.groupby('category_name_english')['product_id'].count().sort_values(ascending=False).reset_index()
        product_count_df.rename(columns={'category_name_english': 'category_name_english', 'product_id': 'product_count'}, inplace=True)
        return product_count_df
def create_customer_rfm(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    customer_rfm_df = df[(df['order_purchase_timestamp'] >= start_date) & (df['order_purchase_timestamp'] <= end_date)]
    customer_rfm_df = customer_rfm_df[['customer_unique_id', 'order_id', 'total_price', 'order_purchase_timestamp']]

    recency_df = customer_rfm_df.groupby('customer_unique_id')['order_purchase_timestamp'].max().reset_index()
    recency_df['recency'] = (end_date - recency_df['order_purchase_timestamp']).dt.days

    frequency_df = customer_rfm_df.groupby('customer_unique_id')['order_id'].count().reset_index()
    frequency_df.rename(columns={'order_id': 'frequency'}, inplace=True)

    monetary_df = customer_rfm_df.groupby('customer_unique_id')['total_price'].sum().reset_index()
    monetary_df.rename(columns={'total_price': 'monetary'}, inplace=True)

    customer_rfm_df = pd.merge(recency_df, frequency_df, on='customer_unique_id', how='left')
    customer_rfm_df = pd.merge(customer_rfm_df, monetary_df, on='customer_unique_id', how='left')

    customer_rfm_df['customer_unique_id'] = customer_rfm_df['customer_unique_id'].str[:5]
    
    return customer_rfm_df

def rfm_score(df):
    df['R_rank'] = df['recency'].rank(ascending=False)
    df['F_rank'] = df['frequency'].rank(ascending=True)
    df['M_rank'] = df['monetary'].rank(ascending=True)
    
    # normalizing the rank of the customers
    df['R_rank_norm'] = (df['R_rank']/df['R_rank'].max())*100
    df['F_rank_norm'] = (df['F_rank']/df['F_rank'].max())*100
    df['M_rank_norm'] = (df['F_rank']/df['M_rank'].max())*100
    
    df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)

    df['RFM_Score'] = 0.15*df['R_rank_norm'] + 0.28*df['F_rank_norm'] + 0.57*df['M_rank_norm']
    df['RFM_Score'] *= 0.05
    df = df.round(2)

    df['customer_unique_id'] = df['customer_unique_id'].str[:5]
    df.drop(columns=['R_rank_norm', 'F_rank_norm', 'M_rank_norm', 'order_purchase_timestamp'], inplace=True)
    df.set_index('customer_unique_id', inplace=True)
    df = df.sort_values(by='RFM_Score', ascending=False)
    return df

# Load the dataset
daily_report_df = pd.read_csv('https://raw.githubusercontent.com/raviearjun/Dicoding-Data-Analisis/main/sum_price_by_orderid.csv')
product_performance_df = pd.read_csv('https://raw.githubusercontent.com/raviearjun/Dicoding-Data-Analisis/main/product_performance_df.csv')

# Format timestamps
daily_report_df['order_purchase_timestamp'] = pd.to_datetime(daily_report_df['order_purchase_timestamp'])
product_performance_df['order_purchase_timestamp'] = pd.to_datetime(product_performance_df['order_purchase_timestamp'])

# Date range
min_date = daily_report_df['order_purchase_timestamp'].min().date()
max_date = daily_report_df['order_purchase_timestamp'].max().date()


# Sidebar
with st.sidebar:
    st.image('https://raw.githubusercontent.com/raviearjun/Dicoding-Data-Analisis/main/logo.png', width=100)
    start_date, end_date = st.date_input(
        label='Date Range',
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

# Streamlit Title
st.title('E-Commerce Public Dataset Analysis')

# Description
st.write('This dashboard provides an overview of the public dataset.')

# Daily Report
st.subheader('Daily Report')
daily_orders_df = create_daily_report(daily_report_df, start_date, end_date)
revenue_daily = daily_orders_df['total_revenue'].sum()
total_orders = len(daily_orders_df)
avg_order_value = daily_orders_df['total_revenue'].mean()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Orders', total_orders)
with col2:
    st.metric('Revenue', format_currency(revenue_daily, 'BRL', locale='pt_BR'))
with col3:
    st.metric('Average Order Value', format_currency(avg_order_value, 'BRL', locale='pt_BR'))


# Daily Revenue Line Chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=daily_orders_df, x='order_purchase_timestamp', y='total_revenue', marker='o', ax=ax)
ax.set_title('Daily Revenue')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Product Performance
st.subheader('Product Performance')
product_performance_filtered = create_product_performance(product_performance_df, start_date, end_date, 'product_count')
col1, col2 = st.columns(2)
with col1:
    st.metric('Total Product Sold', len(product_performance_filtered))
with col2:
    st.metric('Total Product Category', len(product_performance_filtered['category_name_english'].unique()))

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))
sns.barplot(x='product_count', y='category_name_english', data=product_performance_filtered.head(10), palette='deep', ax=ax[0])
ax[0].set_title('Top 10 Products Sold', loc='center', fontsize=16)
ax[0].set_ylabel(None)
ax[0].set_xlabel('Number of Products Sold', fontsize=12)
ax[0].tick_params(axis='x', labelsize=12)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x='product_count', y='category_name_english', data=product_performance_filtered.tail(10), palette='deep', ax=ax[1])
ax[1].set_title('Bottom 10 Products Sold', loc='center', fontsize=16)
ax[1].set_ylabel(None)  
ax[1].set_xlabel('Number of Products Sold', fontsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='x', labelsize=12)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

# Best Customers Based on RFM Analysis
st.subheader('Best Customers Based on RFM Analysis')
customer_rfm_df = create_customer_rfm(product_performance_df, start_date, end_date)
max_date = pd.to_datetime(customer_rfm_df['order_purchase_timestamp'].max().date())
# Filter anomali
customer_rfm_df = customer_rfm_df[customer_rfm_df['order_purchase_timestamp'] <= max_date]

col1, col2, col3  = st.columns(3)
with col1:
    avg_recency_days = round(customer_rfm_df['recency'].mean(), 2) 
    st.metric('Average Recency', avg_recency_days)
with col2:
    avg_frequency = round(customer_rfm_df.groupby('customer_unique_id')['frequency'].count().mean(), 2)
    st.metric('Average Frequency', avg_frequency)
with col3:
    avg_money = round(customer_rfm_df['monetary'].mean(), 2)
    st.metric('Average Monetary', format_currency(avg_money, 'BRL', locale='pt_BR'))

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 6))
recency_customers = customer_rfm_df.sort_values(by='recency', ascending=True).head(5).reset_index(drop=True)
sns.barplot(x='customer_unique_id', y='recency', data=recency_customers, palette='deep', ax=ax[0])
ax[0].set_title('Top 5 Best Customers by Recent', loc='center', fontsize=10)
ax[0].set_ylabel(None)
ax[0].set_xlabel('Customer Unique ID', fontsize=12)
ax[0].tick_params(axis='x', labelsize=12, labelrotation=45)

freq_customers = customer_rfm_df.sort_values(by='frequency', ascending=False).head(5).reset_index()
sns.barplot(x='customer_unique_id', y='frequency', data=freq_customers, palette='deep', ax=ax[1])
ax[1].set_title('Top 5 Best Customers by Frequency', loc='center', fontsize=10)
ax[1].set_ylabel(None)
ax[1].set_xlabel('Customer Unique ID', fontsize=12)
ax[1].tick_params(axis='x', labelsize=12, labelrotation=45)

monetary_customers = customer_rfm_df.sort_values(by='monetary', ascending=False).head(5).reset_index()
sns.barplot(x='customer_unique_id', y='monetary', data=monetary_customers, palette='deep', ax=ax[2])
ax[2].set_title('Top 5 Best Customers by Monetary', loc='center', fontsize=10)
ax[2].set_ylabel(None)
ax[2].set_xlabel('Customer Unique ID', fontsize=12)
ax[2].tick_params(axis='x', labelsize=12, labelrotation=45)
st.pyplot(fig)

# Customer Ranking Based on RFM Analysis
st.subheader('Customer Ranking Based on RFM Analysis')
customer_ranking_df = rfm_score(customer_rfm_df)
st.dataframe(customer_ranking_df.head(10))

# Customer Demographics
st.subheader('Customer Demographics')
customer_demographic_df = create_product_performance(product_performance_df, start_date, end_date, 'customer_demographic')
customer_demographic_df.columns = ['customer_state', 'customer_count']
col1, col2 = st.columns(2)
with col1:
    st.metric('Total Customers', customer_demographic_df['customer_count'].sum())
with col2:
    st.metric('Total States', len(customer_demographic_df['customer_state'].unique()))

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=customer_demographic_df, x='customer_count', y='customer_state', palette='deep', ax=ax)
ax.set_title('Customer Distribution by State')
st.pyplot(fig)

st.caption('Copyright (c) 2023. Ravie Arjun Nadhief. All rights reserved.')
