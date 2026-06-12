import streamlit as st
import pandas as pd
from datetime import date

# પેજ સેટઅપ
st.set_page_config(page_title="Ice Cream Digital Challan", layout="wide")

st.title("🍦 આઈસ્ક્રીમ ડિજિટલ ચલણ બુક")
st.write("---")

# સેઝન સ્ટેટમાં ચલણ નંબર મેન્ટેન કરવા માટે
if "challan_number" not in st.session_state:
    st.session_state.challan_number = 403  # તમારા ફોટા મુજબનો સ્ટાર્ટિંગ નંબર

# ઉપરનો ભાગ: ચલણ નંબર અને તારીખ
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.subheader(f"📄 Delivery Challan No: {st.session_state.challan_number}")
with col_top2:
    challan_date = st.date_input("DATE (તારીખ):", date.today())

# ગ્રાહક અને લોકેશનની વિગત
st.write("### 👤 ગ્રાહકની વિગત")
col_cust1, col_cust2 = st.columns(2)
with col_cust1:
    customer_name = st.text_input("ગ્રાહક / દુકાનનું નામ:")
with col_cust2:
    delivery_place = st.text_input("જગ્યાનું નામ / એડ્રેસ (જેમ કે: ન્યુવીઆઈપી પુરા):")

st.write("---")
st.write("### 🍧 આઈસ્ક્રીમ અને ક્વોન્ટિટી લિસ્ટ")
st.info("💡 જે આઈસ્ક્રીમનો ઓર્ડર હોય તેની જ ક્વોન્ટિટી અને ભાવ લખો. બાકીનામાં 0 રહેવા દો.")

# તમારા ફોટા (image_a1d9ff.jpg) મુજબની બધી જ આઈટમ્સનું લિસ્ટ
ice_cream_items = [
    "Vanila", "American Dryfruit", "Chocolate Chips", "Rajbhog", "Kesar Pista",
    "Anjeer Dryfruit", "Mava Malai", "White House", "Guvava", "Kaju mava Kesar",
    "Natkhat", "Cookies Cream", "Monsun Magic", "Chocolate Belgium", "Mengo",
    "Strawberry", "Golden Pearl", "Butter Scotch", "Roasted Almond", "Pan masala",
    "Roll Cut", "Rajasthani Roll Cut", "Shahi Gulab", "Rajwadi", "kaju Draksh",
    "Maxican Khazana", "Sitafad", "Stick Gulfi-10", "Stick Gulfi-20", "Bhadam Sek",
    "Coco", "Lassi", "Mango Delight", "Fruit Salad"
]

# સ્ક્રીન પર બે ભાગમાં આઈટમ વહેંચવા માટે (ફોટા જેવું જ લુક આપવા)
mid_point = len(ice_cream_items) // 2
left_list = ice_cream_items[:mid_point+1]
right_list = ice_cream_items[mid_point+1:]

order_entries = []

col_list1, col_list2 = st.columns(2)

# ડાબી બાજુની આઈસ્ક્રીમ આઈટમ્સ
with col_list1:
    st.markdown("#### **લિસ્ટ - ૧**")
    for item in left_list:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.write(f"🔹 **{item}**")
        with c2:
            qty = st.number_input("Qty", min_value=0, value=0, step=1, key=f"qty_{item}")
        with c3:
            price = st.number_input("ભાવ (₹)", min_value=0, value=0, step=5, key=f"price_{item}")
        if qty > 0:
            order_entries.append({"Item": item, "Quantity": qty, "Price": price, "Total": qty * price})

# જમણી બાજુની આઈસ્ક્રીમ આઈટમ્સ
with col_list2:
    st.markdown("#### **લિસ્ટ - ૨**")
    for item in right_list:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.write(f"🔹 **{item}**")
        with c2:
            qty = st.number_input("Qty", min_value=0, value=0, step=1, key=f"qty_{item}")
        with c3:
            price = st.number_input("ભાવ (₹)", min_value=0, value=0, step=5, key=f"price_{item}")
        if qty > 0:
            order_entries.append({"Item": item, "Quantity": qty, "Price": price, "Total": qty * price})

st.write("---")

# ફોટા નીચે મુજબની EXTRA ITEM (Box, Drum, Can, Kothi)
st.write("### 📦 EXTRA ITEM (સામાનની વિગત)")
extra_items = ["Box", "Drum", "Can", "Kothi"]
extra_entries = []

col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
columns_list = [col_ex1, col_ex2, col_ex3, col_ex4]

for i, ex_item in enumerate(extra_items):
    with columns_list[i]:
        st.markdown(f"**📦 {ex_item}**")
        given = st.number_input("આપેલ (Given)", min_value=0, value=0, step=1, key=f"given_{ex_item}")
        returned = st.number_input("પાછું આવેલ (Return)", min_value=0, value=0, step=1, key=f"return_{ex_item}")
        if given > 0 or returned > 0:
            extra_entries.append({"Extra Item": ex_item, "Given": given, "Return": returned})

st.write("---")

# બિલની આખરી ગણતરી અને સમરી
st.write("### 🧾 બિલ સમરી (Final Invoice)")

if order_entries:
    # ટેબલ સ્વરૂપે ઓર્ડર બતાવવો
    df = pd.DataFrame(order_entries)
    st.table(df)
    
    grand_total = df["Total"].sum()
    st.markdown(f"## 💰 **કુલ રકમ (Grand Total): ₹ {grand_total}/-**")
    
    # સહી માટેની જગ્યા
    col_sign1, col_sign2 = st.columns(2)
    with col_sign1:
        st.write("✍️ **Auth. Sign (માલિકની સહી):** __________________")
    with col_sign2:
        st.write("✍️ **Receiver Sign (લેનારની સહી):** __________________")
        
    st.write(" ")
    # ચલણ સેવ કરવાનું બટન
    if st.button("💾 ચલણ સેવ કરો અને પ્રિન્ટ કરો"):
        st.success(f"ચલણ નંબર {st.session_state.challan_number} સક્સેસફુલી સેવ થઈ ગયું છે!")
        # સેવ થયા પછી ઓટોમેટિક ચલણ નંબર વધારવા માટે
        st.session_state.challan_number += 1
        st.info("નવું ચલણ બનાવવા માટે પેજ રીફ્રેશ કરો અથવા નવો ઓર્ડર નાખો.")
else:
    st.warning("⚠️ ચલણ બનાવવા માટે લિસ્ટમાંથી કોઈ પણ આઈસ્ક્રીમની 'Qty' (ક્વોન્ટિટી) અને 'ભાવ' ઉમેરો.")
