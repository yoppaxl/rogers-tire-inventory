
import pandas as pd
import streamlit as st

# Load inventory
df = pd.read_csv("rogers_tire_inventory.csv")

st.set_page_config(page_title="Rogers Tire Inventory", layout="centered")
st.title("Rogers Tire Inventory")

# --- Search Section ---
st.subheader("🔍 Search Inventory")
query = st.text_input("Search for a tire size (e.g., 235/65/17):").strip()

if query:
    results = df[df["Tire Size"].str.replace(" ", "").str.lower() == query.replace(" ", "").lower()]
    if not results.empty:
        for _, row in results.iterrows():
            st.success(f"{row['Tire Size']} ({row['Rim Size']}): {row['Quantity']} in stock")
    else:
        st.warning("No matching tire size found.")
else:
    st.info("Enter a tire size to search.")

# --- Add Tire Section ---
st.subheader("➕ Add to Inventory")
add_tire = st.text_input("Tire Size to Add (e.g., 235/65/17)", key="add")
add_rim = st.text_input("Rim Size (e.g., 17's)", key="rim")
add_qty = st.number_input("Quantity to Add", min_value=1, step=1, key="qty_add")
if st.button("Add Tire"):
    mask = (df["Tire Size"].str.lower() == add_tire.lower()) & (df["Rim Size"].str.lower() == add_rim.lower())
    if df[mask].empty:
        df = pd.concat([df, pd.DataFrame([{
            "Tire Size": add_tire, "Rim Size": add_rim, "Quantity": add_qty
        }])], ignore_index=True)
        st.success(f"Added new tire: {add_tire} ({add_rim}) x{add_qty}")
    else:
        df.loc[mask, "Quantity"] += add_qty
        st.success(f"Updated quantity for {add_tire} ({add_rim})")

# --- Remove Tire Section ---
st.subheader("➖ Remove from Inventory")
remove_tire = st.text_input("Tire Size to Remove", key="remove")
remove_rim = st.text_input("Rim Size", key="rim2")
remove_qty = st.number_input("Quantity to Remove", min_value=1, step=1, key="qty_remove")
if st.button("Remove Tire"):
    mask = (df["Tire Size"].str.lower() == remove_tire.lower()) & (df["Rim Size"].str.lower() == remove_rim.lower())
    if df[mask].empty:
        st.error("Tire not found in inventory.")
    else:
        current_qty = df.loc[mask, "Quantity"].values[0]
        if current_qty <= remove_qty:
            df = df[~mask]
            st.success(f"Removed all of {remove_tire} ({remove_rim}) from inventory.")
        else:
            df.loc[mask, "Quantity"] -= remove_qty
            st.success(f"Removed {remove_qty} of {remove_tire} ({remove_rim})")

# --- Full Inventory View ---
st.subheader("📋 Full Tire Inventory List")

# Filter by rim size
rim_filter = st.selectbox("Filter by Rim Size", options=["All"] + sorted(df["Rim Size"].unique().tolist()))

if rim_filter != "All":
    filtered_df = df[df["Rim Size"] == rim_filter]
else:
    filtered_df = df

# Show the table
st.dataframe(filtered_df.sort_values(by=["Rim Size", "Tire Size"]))

# Optional download
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download This View as CSV", csv, "filtered_inventory.csv", "text/csv")
