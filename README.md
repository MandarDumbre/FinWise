<div align="center">

# ⚡ **FinWise**

### *Making Financial Management Smart and Simple*

**A powerful, intelligent financial dashboard built with Streamlit**
Automated transaction categorization, budgeting, anomaly detection & more.

</div>

---

## 🎥 FinWise Demo

<img src="https://drive.google.com/uc?export=view&id=1nGDnFcsMKcZ62h28srNaZYZGicQ3bX8p" alt="FinWise Dashboard Preview" width="920"/>

<p align="center">
  <a href="https://drive.google.com/file/d/1CsBZAoFoACL77MENQTTKPxccrddAGiUZ/view" target="_blank">
    ▶️ <strong>Watch the Full Video Demo</strong>
  </a>
</p>

---


🛠️ Built With
<p align="center"> <img alt="Python" src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" /> <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit&logoColor=white" /> <img alt="NumPy" src="https://img.shields.io/badge/NumPy-Scientific_Computing-013243?logo=numpy&logoColor=white" /> <img alt="Pandas" src="https://img.shields.io/badge/Pandas-Data_Processing-150458?logo=pandas&logoColor=white" /> <img alt="Plotly" src="https://img.shields.io/badge/Plotly-Interactive_Charts-3f4f75?logo=plotly&logoColor=white" /> <img alt="CSV" src="https://img.shields.io/badge/CSV-Data_Format-yellow?logo=file&logoColor=white" /> <img alt="CSS" src="https://img.shields.io/badge/Custom_CSS-Theming-purple?logo=css3&logoColor=white" /> </p> </div>

---

## 🚀 Features

| 🔧 Feature                  | ⚡ Description                                                   |
| --------------------------- | --------------------------------------------------------------- |
| 📊 **Smart Categorization** | Regex-based transaction tagging using rule-based classification |
| 💰 **Budget Tracking**      | Set and monitor monthly limits for different categories         |
| 🚨 **Anomaly Detection**    | Detect outlier spendings using Z-score-based analysis           |
| 📈 **Advanced Analytics**   | Interactive charts for trends and category-wise spends          |
| 🔍 **Dynamic Filtering**    | Filter by date range and spending categories                    |
| 💡 **Smart Insights**       | AI-powered spending insights and financial recommendations      |
| 📱 **Responsive Design**    | Clean, modern UI built with mobile-first design in mind         |
| 📥 **Data Export**          | Export filtered transactions to CSV                             |

---

## 🛠️ Technology Stack

```text
Frontend       : Streamlit
Data Handling  : Pandas, NumPy
Visualization  : Plotly
Styling        : Custom CSS (gradient themes)
File Format    : CSV
```

---

## 📋 Prerequisites

* Python 3.8+
* pip (Python package manager)

---

## 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/MandarDumbre/finwise.git
cd finwise

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🧠 Categorization Rules

Create a file called `categories.json` in the root directory:

```json
{
  "Food & Dining": ["swiggy", "zomato", "restaurant", "cafe", "food"],
  "Transportation": ["uber", "ola", "petrol", "metro", "taxi"],
  "Shopping": ["amazon", "flipkart", "mall", "shopping"],
  "Utilities": ["electricity", "water", "gas", "internet"],
  "Healthcare": ["hospital", "pharmacy", "doctor", "medicine"],
  "Entertainment": ["netflix", "movie", "cinema", "gaming"],
  "Income": ["salary", "bonus", "dividend", "interest"]
}
```

---

## ▶️ Run the App

```bash
streamlit run finwise.py
```

---

## 📊 Data Format

| Column         | Format        | Description                            |
| -------------- | ------------- | -------------------------------------- |
| `Date`         | `DD Mon YYYY` | Transaction date (e.g., `15 Jan 2024`) |
| `Details`      | `Text`        | Description of the transaction         |
| `Amount`       | `Float`       | Amount (numeric, no currency symbol)   |
| `Debit/Credit` | `Text`        | Either `"Debit"` or `"Credit"`         |

**Sample:**

```csv
Date,Details,Amount,Debit/Credit
15 Jan 2024,Swiggy Order - Pizza,450.00,Debit
16 Jan 2024,Salary Credit,75000.00,Credit
17 Jan 2024,Uber Ride,120.50,Debit
```

---

## 🎯 Usage Guide

1. **📁 Upload your transaction file**

   * Choose your `.csv` file with the above format

2. **📊 Set Budgets**

   * Use sidebar sliders to assign monthly budgets per category

3. **📈 Explore Analytics**

   * Navigate tabs for:

     * 💸 Expenses
     * 💰 Income
     * 📊 Analytics
     * 📈 Insights
     * 🚨 Anomalies

4. **🧹 Filter & Export**

   * Use filters by category and date
   * Click to download filtered results

---

## 🗂️ Project Structure

```bash
finwise/
├── finwise.py               # Streamlit app
├── data_generator.py        # Optional test data generator
├── categories.json          # Categorization rules
├── requirements.txt         # Dependencies
├── README.md                # This file
└── sample_data/             # Sample CSV data
```

---

## 🧪 Sample Data Generator

Generate realistic financial data:

```bash
python data_generator.py
```

Produces `finwise_sample_data_3months.csv` with:

* 3 months of transactions
* Multiple categories
* Anomalies and variations
* Salary & recurring spends

---

## 🔧 Customization

### ➕ Add New Categories

```json
{
  "Education": ["udemy", "coursera", "edx", "fee", "exam"]
}
```

### 🎯 Tune Anomaly Detection

In `detect_anomalies()`:

```python
threshold_zscore = 2.5  # Adjust 1.5–3.0 for more/less sensitivity
```

---

## 📈 Analytics Overview

| 🔍 Chart Type         | 📌 Purpose                              |
| --------------------- | --------------------------------------- |
| 📉 Daily Trends       | Line chart of day-wise spend            |
| 🧩 Category Breakdown | Pie chart of category-wise distribution |
| 🥇 Top Categories     | Bar chart of most spent areas           |

### 🤖 Smart Insights Engine

* Budget health summary
* Spending habits & overages
* Anomaly explanations
* Pattern recognition

---

## 🛡️ Security & Privacy

✔ All processing is **local**
✔ No financial data is **stored**
✔ Session-based, **ephemeral data handling**

---

## 🤝 Contributing

We welcome PRs and feature suggestions! 💬

```bash
# Fork > Branch > Code > Commit > PR
git checkout -b feature/AmazingFeature
```

---

## 🐛 Known Issues

* Large files (>10k records) may slow down processing
* Date formats must follow `DD Mon YYYY` or `YYYY-MM-DD`

---

## 🔮 Roadmap

* [ ] Multi-currency support 💱
* [ ] ML-based categorization 🧠
* [ ] Export to PDF 📄
* [ ] Mobile App 📱
* [ ] Bank API integration 🔗
* [ ] Goal-based savings tracker 🎯

---

## 📝 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

* [Streamlit](https://streamlit.io)
* [Plotly](https://plotly.com)
* [Pandas](https://pandas.pydata.org)

---

<div align="center">

⭐ **Star this repo** • 🐛 [Report Bug](https://github.com/MandarDumbre/finwise/issues) • ✨ [Request Feature](https://github.com/MandarDumbre/finwise/issues)

</div>

---

Let me know if you'd like an actual banner image or contributor badges added too.
