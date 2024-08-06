import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import DataAnalyze, MapPlotBrazil

# Set Seaborn style and Streamlit option
sns.set(style='dark')

# Load dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
ecommerce_data = pd.read_csv('https://raw.githubusercontent.com/zaimirfansyah/data-analysis-using-python/main/dashboard/df.csv')
ecommerce_data.sort_values(by="order_approved_at", inplace=True)
ecommerce_data.reset_index(drop=True, inplace=True)

# Load geolocation dataset
geolocation_data = pd.read_csv('https://raw.githubusercontent.com/zaimirfansyah/data-analysis-using-python/main/dashboard/geo.csv')
unique_geolocations = geolocation_data.drop_duplicates(subset='customer_unique_id')

# Convert datetime columns
for col in datetime_cols:
    ecommerce_data[col] = pd.to_datetime(ecommerce_data[col])

# Get min and max dates for filtering
start_date = ecommerce_data["order_approved_at"].min()
end_date = ecommerce_data["order_approved_at"].max()

# Sidebar setup
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image('https://raw.githubusercontent.com/zaimirfansyah/data-analysis-using-python/main/dashboard/logo.png', width=100)
    with col3:
        st.write(' ')

    # Date range selection
    selected_start_date, selected_end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        value=[start_date, end_date],
        min_value=start_date,
        max_value=end_date
    )

# Filter main dataframe based on selected date range
filtered_data = ecommerce_data[(ecommerce_data["order_approved_at"] >= str(selected_start_date)) & 
                               (ecommerce_data["order_approved_at"] <= str(selected_end_date))]

# Initialize analysis and mapping classes
analysis = DataAnalyze(filtered_data)
map_plotter = MapPlotBrazil(unique_geolocations, plt, mpimg, urllib, st)

# Generate dataframes for analysis
daily_orders = analysis.generate_daily_orders()
daily_spend = analysis.generate_daily_spend()
order_items_summary = analysis.summarize_order_items()
review_scores, most_frequent_score = analysis.get_review_scores()
state_distribution, top_state = analysis.customer_distribution_by_state()
order_status_distribution, top_status = analysis.order_status_summary()

# Streamlit app layout
st.title("Analisa Data : E Commerce Public ")
st.write("**Dashboard untuk Analisa Data pada E Commerce Public .**")

# Daily Orders Delivered section
st.subheader("Pesanan harian diterima")
col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders["order_count"].sum()
    st.markdown(f"Total Pesanan: **{total_orders}**")

with col2:
    total_revenue = daily_orders["revenue"].sum()
    st.markdown(f"Total Pendapatan: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders["order_approved_at"],
    y=daily_orders["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
    ax=ax
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Customer Spend Money section
st.subheader("Pengeluaran oleh Pelanggan")
col1, col2 = st.columns(2)

with col1:
    total_spend = daily_spend["total_spend"].sum()
    st.markdown(f"Total Pengeluaran: **{total_spend}**")

with col2:
    average_spend = daily_spend["total_spend"].mean()
    st.markdown(f"Rata-rata Pengeluaran: **{average_spend}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=daily_spend,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#90CAF9",
    ax=ax
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items section
st.subheader("Item Pesanan")
col1, col2 = st.columns(2)

with col1:
    total_items_sold = order_items_summary["product_count"].sum()
    st.markdown(f"Total Item terjual: **{total_items_sold}**")

with col2:
    average_items_sold = order_items_summary["product_count"].mean()
    st.markdown(f"Rata-rata Item terjual: **{average_items_sold}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="product_count", y="product_category_name_english", data=order_items_summary.head(5), palette="viridis", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Penjualan", fontsize=80)
ax[0].set_title("Produk Terlaris", loc="center", fontsize=90)
ax[0].tick_params(axis='y', labelsize=55)
ax[0].tick_params(axis='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", data=order_items_summary.tail(5), palette="viridis", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Penjualan", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling tidak laku", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

# Review Score section
st.subheader("Skor Review")
col1, col2 = st.columns(2)

with col1:
    average_review_score = review_scores.mean()
    st.markdown(f"Rata-rata Skor: **{average_review_score:.2f}**")

with col2:
    most_common_review_score = most_frequent_score
    st.markdown(f"Skor Paling umum: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", len(review_scores))

sns.barplot(x=review_scores.index,
            y=review_scores.values,
            order=review_scores.index,
            palette=colors,
            ax=ax)

plt.title("Skor review oleh pelanggan", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Total")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add labels on top of each bar
for i, v in enumerate(review_scores.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig)

# Customer Demographic section
st.subheader("Demografi Pelanggan")
tab1, tab2 = st.tabs(["State", "Geo lokasi"])

with tab1:
    st.markdown(f"Most Common State: **{top_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state_distribution["customer_state"],
                y=state_distribution["customer_count"], 
                palette="viridis",
                ax=ax)

    plt.title("Jumlah pelanggan berdasarkan state", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Jumlah pelanggan")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    map_plotter.plot_map() 

    with st.expander("lihat selengkapnya"):
        st.write('Menurut grafik, ada lebih banyak pelanggan di wilayah tenggara dan selatan. Selain itu, ada lebih banyak pelanggan di ibu kota seperti São Paulo, Rio de Janeiro, Porto Alegre, dll.')
