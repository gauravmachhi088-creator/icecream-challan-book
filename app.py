import streamlit as st
import pandas as pd
from datetime import date

# Page Setup
st.set_page_config(page_title="Ice Cream Digital Challan", layout="wide")

st.title("🍦 Ice Cream Digital Challan Book")
st.write("---")

# Maintain Challan Number in Session State
if "challan_number" not in st.session_state:
    st.session_state.challan_number = 403  # Starting number from your photo

# Top Section: Challan No & Date
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.subheader(f"📄 Delivery Challan No: {st.session_state.challan_number}")
with col_top2:
    challan_date = st.date_input("DATE:", date.today())

# Customer Details
st.write("### 👤 Customer Details")
col_cust1, col_cust2 = st.columns(2)
with col_cust1:
    customer_name = st.text_input("Customer / Shop Name:")
with col_cust2:
    delivery_place = st.text_input("Delivery Place / Address (e.g., New VIP Pura):")

st.write("---")
st.write("### 🍧 Ice Cream & Quantity List")
st.info("💡 Enter Quantity and Price only for the items ordered. Leave others as 0.")

# All 34 items from your photo
ice_cream_items = [
    "Vanila", "American Dryfruit", "Chocolate Chips", "Rajbhog", "Kesar Pista",
    "Anjeer Dryfruit", "Mava Malai", "White House", "Guvava", "Kaju mava Kesar",
    "Natkhat", "Cookies Cream", "Monsun Magic", "Chocolate Belgium", "Mengo",
    "Strawberry", "Golden Pearl", "Butter Scotch", "Roasted Almond", "Pan masala",
    "Roll Cut", "Rajasthani Roll Cut", "Shahi Gulab", "Rajwadi", "kaju Draksh",
    "Maxican Khazana", "Sitafad", "Stick Gulfi-10", "Stick Gulfi-20", "Bhadam Sek",
    "Coco", "Lassi", "Mango Delight", "Fruit Salad"
]

mid_point = len(ice_cream_items) // 2
left_list = ice_cream_items[:mid_point+1]
right_list = ice_cream_items[mid_point+1:]

order_entries = []
col_list1, col_list2 = st.columns(2)

# Left Side Items
with col_list1:
    st.markdown("#### **List - 1**")
    for item in left_list:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.write(f"🔹 **{item}**")
        with c2:
            qty = st.number_input("Qty", min_value=0, value=0, step=1, key=f"qty_{item}")
        with c3:
            price = st.number_input("Rate (₹)", min_value=0, value=0, step=5, key=f"price_{item}")
        if qty > 0:
            order_entries.append({"Item Name": item, "Quantity": qty, "Rate": price, "Total Amount": qty * price})

# Right Side Items
with col_list2:
    st.markdown("#### **List - 2**")
    for item in right_list:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.write(f"🔹 **{item}**")
        with c2:
            qty = st.number_input("Qty", min_value=0, value=0, step=1, key=f"qty_{item}")
        with c3:
            price = st.number_input("Rate (₹)", min_value=0, value=0, step=5, key=f"price_{item}")
        if qty > 0:
            order_entries.append({"Item Name": item, "Quantity": qty, "Rate": price, "Total Amount": qty * price})

st.write("---")

# EXTRA ITEM Section
st.write("### 📦 EXTRA ITEM DETAILS")
extra_items = ["Box", "Drum", "Can", "Kothi"]
extra_entries = []

col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
columns_list = [col_ex1, col_ex2, col_ex3, col_ex4]

for i, ex_item in enumerate(extra_items):
    with columns_list[i]:
        st.markdown(f"**📦 {ex_item}**")
        given = st.number_input("Given", min_value=0, value=0, step=1, key=f"given_{ex_item}")
        returned = st.number_input("Return", min_value=0, value=0, step=1, key=f"return_{ex_item}")
        if given > 0 or returned > 0:
            extra_entries.append({"Extra Item": ex_item, "Given": given, "Return": returned})

st.write("---")

# Invoice Summary
st.write("### 🧾 Final Invoice Summary")

if order_entries:
    df = pd.DataFrame(order_entries)
    st.table(df)
    
    grand_total = df["Total Amount"].sum()
    st.markdown(f"## 💰 **Grand Total: ₹ {grand_total}/-**")
    
    col_sign1, col_sign2 = st.columns(2)
    with col_sign1:
        st.write("✍️ **Auth. Sign:** __________________")
    with col_sign2:
        st.write("✍️ **Receiver Sign:** __________________")
        
    st.write(" ")
    if st.button("💾 Save & Print Challan"):
        st.success(f"Challan No. {st.session_state.challan_number} saved successfully!")
        st.session_state.challan_number += 1
        st.info("Refresh or create a new order to update the view.")
else:
    st.warning("⚠️ Please enter 'Qty' and 'Rate' for at least one ice cream to generate a challan.")