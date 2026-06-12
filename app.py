import streamlit as st
import pandas as pd
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

# Page Setup
st.set_page_config(page_title="Ice Cream Digital Challan", layout="wide")

# Function to generate PDF Invoice
def generate_pdf_invoice(challan_no, challan_date, customer_name, delivery_place, order_data, extra_data, grand_total):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        alignment=1  # center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=4
    )
    
    # Add title
    story.append(Paragraph("🍦 Ice Cream Digital Challan Book", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add challan details
    details_data = [
        ["Challan No:", str(challan_no), "Date:", str(challan_date)],
        ["Customer Name:", customer_name, "Delivery Place:", delivery_place]
    ]
    details_table = Table(details_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Add items table
    if order_data:
        story.append(Paragraph("Items Ordered:", heading_style))
        items_table_data = [["Item Name", "Quantity", "Rate (₹)", "Total Amount (₹)"]]
        for item in order_data:
            items_table_data.append([
                item["Item Name"],
                str(item["Quantity"]),
                str(item["Rate"]),
                str(item["Total Amount"])
            ])
        items_table = Table(items_table_data, colWidths=[3*inch, 1*inch, 1*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Add extra items if any
    if extra_data:
        story.append(Paragraph("Extra Items:", heading_style))
        extra_table_data = [["Item", "Given", "Return"]]
        for item in extra_data:
            extra_table_data.append([
                item["Extra Item"],
                str(item["Given"]),
                str(item["Return"])
            ])
        extra_table = Table(extra_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        extra_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
        ]))
        story.append(extra_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Add grand total
    story.append(Paragraph(f"<b>Grand Total: ₹ {grand_total}/-</b>", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Add signature lines
    sig_data = [["Auth. Sign: ___________", "Receiver Sign: ___________"]]
    sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10)
    ]))
    story.append(sig_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

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
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("💾 Save & Print Challan"):
            # Generate PDF
            pdf_buffer = generate_pdf_invoice(
                st.session_state.challan_number,
                challan_date,
                customer_name,
                delivery_place,
                order_entries,
                extra_entries,
                grand_total
            )
            st.success(f"✅ Challan No. {st.session_state.challan_number} generated successfully!")
            st.session_state.challan_number += 1
    
    with col_btn2:
        if order_entries:  # Only show download if there are items
            pdf_buffer = generate_pdf_invoice(
                st.session_state.challan_number,
                challan_date,
                customer_name,
                delivery_place,
                order_entries,
                extra_entries,
                grand_total
            )
            st.download_button(
                label="📥 Download Invoice (PDF)",
                data=pdf_buffer,
                file_name=f"challan_{st.session_state.challan_number}.pdf",
                mime="application/pdf"
            )
else:
    st.warning("⚠️ Please enter 'Qty' and 'Rate' for at least one ice cream to generate a challan.")