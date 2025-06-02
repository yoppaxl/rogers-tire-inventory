
import pandas as pd
import streamlit as st

# Load the tire inventory CSV
df = pd.read_csv("rogers_tire_inventory.csv")

st.set_page_config(page_title="Rogers Tire Inventory", layout="centered")
st.title("Rogers Tire Inventory")

# Search bar
query = st.text_input("Search for a tire size (e.g., 235/65/17):").strip()

# Show results
if query:
    results = df[df["Tire Size"].str.replace(" ", "").str.lower() == query.replace(" ", "").lower()]
    if not results.empty:
        for _, row in results.iterrows():
            st.success(f"{row['Tire Size']} ({row['Rim Size']}): {row['Quantity']} in stock")
    else:
        st.warning("No matching tire size found.")
else:
    st.info("Enter a tire size to search.")
