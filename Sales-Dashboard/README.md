# 📊 Sales Dashboard Project

A Python-based sales analysis project with multiple KPIs, visualizations, and forecasts.  
This project uses **pandas, numpy, matplotlib, scikit-learn, statsmodels** to analyze sales data and generate insights.

---

## 📂 Dataset
The dataset used is `sales_data.csv` inside the **Data/** folder.

- **Key columns:**
  - `order_date` – Date of the order
  - `category` – Product category
  - `sku_name` – Product name
  - `qty_ordered` – Quantity ordered
  - `customer_id` – Unique customer ID
  - `registered_date` – Date customer registered
  - `is_valid, is_net, is_gross` – Validation & sales type flags
  - `before_discount, after_discount` – Revenue before/after discount
  - `cogs` – Cost of goods sold
  - `discount_amount` – Discount applied
  - `payment_method` – Payment method used

👉 You can replace the CSV with your own dataset, but keep the same column names so the scripts work.

---

## ⚡ KPIs & Tasks Covered
- **Task 1:** Top 5 products → Mobiles & Tablets (2022)  
- **Task 2:** Sales decrease → “Others” category (2021 → 2022)  
- **Task 4:** Weekend vs Weekday averages → Q4 2022  
- **Task 5:** Largest decrease between two periods  
- **Task 6:** Category trends → Sales trends by category (2022)  
- **Task 7:** Forecast → Predict total sales for Q2 2023  
- **Task 8:** Revenue before vs after discount → By category  
- **Task 9:** Average Order Value (AOV) → Monthly trend (2022)  
- **Task 10:** Payment method performance → Revenue, quantity, net profit  
- **Task 11:** Customer profitability segments → Low / Medium / High  
- **Task 12:** Net profit by category  
- **Task 13:** Unique vs repeat customers (2022)  
- **Task 14:** Time from registration to first order  
- **Task 15:** Sales by discount range  
- **Task 16:** Monthly growth vs discount rate  
- **Task 17:** Average quantity sold per category  

---

## ▶️ How to Run

1. **Clone this repo**
   ```bash
   git clone https://github.com/HeyChamp29/sales-dashboard-project.git
   cd sales-dashboard-project/Sales-Dashboard

python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

python task1.py
python task7.py

📸 Screenshots
All generated charts are stored in the output/ folder.
Example:

(Add more as you generate them!)
🛠 Tech Stack
Python 3
pandas
numpy
matplotlib
scikit-learn
statsmodels
👤 Author
Aman Shah
GitHub: @HeyChamp29
Email: amanshah2916@gmail.com


