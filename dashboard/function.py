import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib
import streamlit as st

class DataAnalyze:
    def __init__(self, df):
        self.df = df

    def generate_daily_orders(self):
        daily_orders = self.df.resample('D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        }).reset_index().rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        })
        return daily_orders

    def generate_daily_spend(self):
        daily_spend = self.df.resample('D', on='order_approved_at').agg({
            "payment_value": "sum"
        }).reset_index().rename(columns={
            "payment_value": "total_spend"
        })
        return daily_spend

    def summarize_order_items(self):
        item_summary = self.df.groupby("product_category_name_english")["product_id"].count().reset_index().rename(columns={
            "product_id": "product_count"
        }).sort_values(by='product_count', ascending=False)
        return item_summary

    def get_review_scores(self):
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        top_score = review_scores.idxmax()
        return review_scores, top_score

    def customer_distribution_by_state(self):
        state_distribution = self.df.groupby("customer_state")["customer_id"].nunique().reset_index().rename(columns={
            "customer_id": "customer_count"
        }).sort_values(by='customer_count', ascending=False)
        top_state = state_distribution.loc[state_distribution['customer_count'].idxmax(), 'customer_state']
        return state_distribution, top_state

    def order_status_summary(self):
        status_summary = self.df["order_status"].value_counts().sort_values(ascending=False)
        top_status = status_summary.idxmax()
        return status_summary, top_status

class MapPlotBrazil:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot_map(self):
        brazil_map = self.mpimg.imread(self.urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10, 10), alpha=0.3, s=0.3, c='maroon')
        self.plt.axis('off')
        self.plt.imshow(brazil_map, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
        self.st.pyplot()
