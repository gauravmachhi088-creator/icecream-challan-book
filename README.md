# 🍦 Ice Cream Digital Challan Book

A Streamlit-based digital invoice/challan system for ice cream shops. Generate and download professional PDF invoices instantly.

## Features

✅ **Digital Challan Management** - Create and manage delivery challans  
✅ **Invoice Generation** - Auto-generate professional PDF invoices  
✅ **PDF Download** - Download invoices for printing or sharing  
✅ **Auto Numbering** - Sequential challan number tracking  
✅ **Extra Items Tracking** - Monitor boxes, drums, cans, and containers  
✅ **Clean UI** - Mobile-friendly, responsive design  

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/gauravmachhi088-creator/icecream-challan-book.git
cd icecream-challan-book
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. Push code to GitHub (already done ✅)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"**
5. Select:
   - **Repository:** `gauravmachhi088-creator/icecream-challan-book`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Click **"Deploy"**

Your app will be live at: `https://share.streamlit.io/gauravmachhi088-creator/icecream-challan-book`

### Option 2: Railway (Paid - $5/month)

1. Go to [railway.app](https://railway.app)
2. Create new project → Import from GitHub
3. Select this repository
4. Add environment: `STREAMLIT_SERVER_HEADLESS=true`
5. Deploy

### Option 3: Render (Free tier available)

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port=10000`
6. Deploy

## Usage

1. **Enter Customer Details**
   - Customer/Shop Name
   - Delivery Place/Address

2. **Select Ice Cream Items**
   - Enter Quantity and Rate (₹)
   - Only items with Qty > 0 will be included

3. **Track Extra Items**
   - Track given/returned boxes, drums, cans, containers

4. **Generate Invoice**
   - Click "Save & Print Challan"
   - Click "📥 Download Invoice (PDF)"

## Dependencies

- `streamlit` - Web app framework
- `pandas` - Data handling
- `reportlab` - PDF generation

## File Structure

```
icecream-challan-book/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # This file
```

## License

MIT License - Feel free to use and modify!

## Support

For issues or suggestions, please create an issue on GitHub.

---

**Made with ❤️ for ice cream shop management**
