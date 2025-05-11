import streamlit as st
import pandas as pd
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.customer_profiler import CustomerProfiler
from agents.emotional_analyzer import EmotionalAnalyzer
from agents.recommendation_engine import RecommendationEngine
from agents.social_proof_engine import SocialProofEngine
from agents.discount_engine import DiscountEngine

CUSTOMER_DATA_PATH = "data/customer_data_collection.csv"
PRODUCT_DATA_PATH = "data/product_recommendation_data.csv"

@st.cache_data
def load_customer_data():
    return pd.read_csv(CUSTOMER_DATA_PATH)

@st.cache_data
def load_product_data():
    return pd.read_csv(PRODUCT_DATA_PATH)

customer_data = load_customer_data()
product_data = load_product_data()

# --- Instantiate agents ---
customer_profiler = CustomerProfiler(CUSTOMER_DATA_PATH)
emotional_analyzer = EmotionalAnalyzer()
recommendation_engine = RecommendationEngine(PRODUCT_DATA_PATH)
social_proof_engine = SocialProofEngine(PRODUCT_DATA_PATH)
discount_engine = DiscountEngine(PRODUCT_DATA_PATH)

# --- Styles (Improved CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
.header {
    background: linear-gradient(90deg, #2874f0, #ec008c);
    padding: 1rem;
    color: #fff;
    font-weight: 700;
    font-size: 2rem;
    text-align: center;
    border-radius: 8px;
    user-select: none;
}
.sidebar-profile, .trending-products, .discounted-products {
    padding: 1rem;
    margin-bottom: 1rem;
    background-color: #f7f7f7;
    border-radius: 10px;
}
.senti-box {
    background: #fce4ec;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #c2185b;
    font-weight: 600;
    margin-top: 0.6rem;
    user-select: none;
}
.category-btns button {
    background: #eee;
    border: none;
    border-radius: 20px;
    padding: 0.4rem 1rem;
    margin-right: 0.5rem;
    cursor: pointer;
    font-weight: 600;
    color: #444;
    transition: all 0.3s ease;
}
.category-btns button.active, .category-btns button:hover {
    background: #2874f0;
    color: white;
}
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    max-height: 520px;
    overflow-y: auto;
    padding-right: 0.5rem;
}
.product-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 5px 10px rgb(0 0 0 / 0.1);
    display: flex;
    flex-direction: column;
    user-select: none;
    transition: box-shadow 0.3s ease;
}
.product-card:hover {
    box-shadow: 0 8px 18px rgb(0 0 0 / 0.15);
}
.product-image {
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    max-height: 160px;
    object-fit: contain;
    width: 100%;
    background: #fafafa;
}
.product-info {
    padding: 0.8rem 1rem;
    flex-grow: 1;
}
.product-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.3rem;
    flex-grow: 1;
}
.product-price {
    font-weight: 700;
    color: #2874f0;
    margin-bottom: 0.3rem;
}
.product-discount {
    font-weight: 600;
    color: #d32f2f;
}
.social-proof {
    font-size: 0.8rem;
    color: #555;
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
}
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background-color: #2874f0;
    border-radius: 3px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header">ShopSmart — Hyper Personalized Shopping</div>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    st.subheader("Customer Profile")

    customer_ids = customer_data["Customer_ID"].tolist()
    selected_customer = st.selectbox("Select Customer", customer_ids)

    profile = customer_profiler.get_customer_profile(selected_customer)
    if profile:
        st.write(f"**Age:** {profile.get('Age', 'NA')}")
        st.write(f"**Gender:** {profile.get('Gender', 'NA')}")
        st.write(f"**Location:** {profile.get('Location', 'NA')}")
        st.write(f"**Customer Segment:** {profile.get('Customer_Segment', 'NA')}")
        st.write(f"**Avg Order Value:** ${profile.get('Avg_Order_Value', 'NA')}")
        st.write(f"**Holiday:** {profile.get('Holiday', 'NA')}")
        st.write(f"**Season:** {profile.get('Season', 'NA')}")

        mood = emotional_analyzer.analyze_emotion(profile)
        st.markdown(f'<div class="senti-box">Current Mood: {mood}</div>', unsafe_allow_html=True)

    else:
        st.write("Customer profile not found.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Visual Search Placeholder
    st.subheader("🔍 Visual Search")
    uploaded_file = st.file_uploader("Upload product image (coming soon!)", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.info("Visual search functionality will be implemented soon.")

# --- Main content ---
search_query = st.text_input("Search for products, brands, and more")
categories = ["all"] + sorted(product_data["Category"].unique())
col1, _ = st.columns([6, 1])
category_index = col1.selectbox("Filter by Category", categories, index=0)

# Filter products
filtered_products = product_data

if category_index != "all":
    filtered_products = filtered_products[filtered_products["Category"] == category_index]

if search_query.strip():
    filtered_products = filtered_products[
        filtered_products["Brand"].str.contains(search_query, case=False, na=False) |
        filtered_products["Product_ID"].astype(str).str.contains(search_query, na=False) |
        filtered_products["Category"].str.contains(search_query, case=False, na=False)
    ]

# Recommended products based on profile
st.subheader(f"Recommended Products for {selected_customer}")

recommendations = recommendation_engine.recommend(profile) if profile is not None else []
if recommendations:
    recommended_df = pd.DataFrame(recommendations)
else:
    recommended_df = pd.DataFrame()

def render_product_card(prod):
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    st.image(prod.get("image_url", "https://via.placeholder.com/150"), use_column_width=True)
    st.markdown('<div class="product-info">', unsafe_allow_html=True)
    st.markdown(f'<div class="product-title">{prod.get("Brand", "")} - {prod.get("Category", "")}</div>', unsafe_allow_html=True)
    price = prod.get("Price", 0)
    discount = prod.get("Discount", 0)
    discounted = price * (1 - discount / 100)
    st.markdown(f'<div class="product-price">₹{discounted:.2f}</div>', unsafe_allow_html=True)
    if discount > 0:
        st.markdown(f'<div class="product-discount">{discount:.0f}% OFF</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if not recommended_df.empty:
    cols = st.columns(4)
    for i, prod in enumerate(recommendations):
        with cols[i % 4]:
            render_product_card(prod)
else:
    st.write("No recommendations available.")

# Trending products
st.subheader("🔥 Trending Products")
trending_products = social_proof_engine.trending()
cols = st.columns(4)
for i, prod in enumerate(trending_products):
    with cols[i % 4]:
        render_product_card(prod)

# Discounted products
st.subheader("🎁 Discounted Products")
discounted_products = discount_engine.discounted()
cols = st.columns(4)
for i, prod in enumerate(discounted_products):
    with cols[i % 4]:
        render_product_card(prod)

# Footer
st.markdown(
    """
    <div style="text-align:center; color:#777; margin-top: 2rem; user-select:none;">
    © 2024 ShopSmart - Inspired by Flipkart and Myntra
    </div>
    """, unsafe_allow_html=True)
