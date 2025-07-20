import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Set random seed for reproducible data
random.seed(42)
np.random.seed(42)

# Define date range (3 months: November 2024 to January 2025)
start_date = datetime(2024, 11, 1)
end_date = datetime(2025, 1, 31)

# Category-wise transaction templates with realistic details
transaction_templates = {
    "Food & Dining": [
        ("Swiggy Order - Pizza Palace", 450, 850),
        ("Zomato - KFC Delivery", 320, 650),
        ("McDonald's Drive Thru", 280, 450),
        ("Cafe Coffee Day", 150, 300),
        ("Restaurant Booking - The Spice Route", 1200, 2500),
        ("Subway Fresh Meal", 200, 400),
        ("Local Dhaba", 80, 200),
        ("Starbucks Coffee", 250, 450),
        ("Domino's Pizza Order", 380, 750),
        ("Haldiram's Snacks", 120, 300)
    ],
    
    "Groceries": [
        ("Reliance Fresh - Monthly Grocery", 2500, 4500),
        ("DMart Hypermarket", 1800, 3200),
        ("BigBasket Online Order", 1200, 2200),
        ("Local Kirana Store", 300, 800),
        ("Zepto Quick Delivery", 150, 400),
        ("Spencer's Retail", 800, 1500),
        ("More Supermarket", 600, 1200),
        ("Fresh Fruits & Vegetables", 200, 500)
    ],
    
    "Transportation": [
        ("Uber Ride", 120, 450),
        ("Ola Cab Service", 85, 380),
        ("Petrol - HP Gas Station", 2000, 3500),
        ("Delhi Metro Card Recharge", 200, 500),
        ("Auto Rickshaw", 30, 120),
        ("Bus Ticket", 15, 50),
        ("Rapido Bike Taxi", 45, 150),
        ("Diesel Fill - IOCL", 2800, 4200)
    ],
    
    "Shopping": [
        ("Amazon Online Purchase", 800, 2500),
        ("Flipkart Fashion Sale", 1200, 3000),
        ("Myntra Clothing", 900, 2200),
        ("Zara Store Purchase", 2500, 6000),
        ("H&M Fashion", 1500, 3500),
        ("Local Electronics Store", 5000, 15000),
        ("Nike Store", 3200, 8000),
        ("Adidas Showroom", 2800, 7000),
        ("Lifestyle Store", 1800, 4500)
    ],
    
    "Utilities": [
        ("Electricity Bill - BSES", 1200, 2500),
        ("Water Bill - DJB", 300, 800),
        ("Jio Fiber Internet", 699, 1299),
        ("Airtel Mobile Recharge", 299, 599),
        ("Gas Cylinder - HP", 850, 950),
        ("Broadband Bill", 800, 1500),
        ("DTH Recharge - Tata Sky", 350, 650)
    ],
    
    "Healthcare": [
        ("Apollo Pharmacy", 250, 800),
        ("Doctor Consultation Fee", 500, 1200),
        ("Max Hospital Bill", 2500, 8000),
        ("Dental Clinic Visit", 800, 2000),
        ("Medicine Purchase", 180, 600),
        ("Health Checkup Package", 3000, 6000),
        ("Physiotherapy Session", 600, 1200)
    ],
    
    "Entertainment": [
        ("Netflix Subscription", 199, 649),
        ("BookMyShow Movie Tickets", 280, 600),
        ("Spotify Premium", 119, 179),
        ("PVR Cinema", 350, 800),
        ("Gaming Purchase - Steam", 500, 2000),
        ("Concert Tickets", 1500, 5000),
        ("Amazon Prime Video", 129, 999)
    ],
    
    "Travel": [
        ("IndiGo Flight Booking", 4500, 12000),
        ("Hotel Booking - OYO", 1200, 3500),
        ("MakeMyTrip Package", 8000, 25000),
        ("Railway Ticket Booking", 450, 1200),
        ("Goibibo Hotel", 2200, 5500),
        ("Agoda Accommodation", 3500, 8000)
    ],
    
    "Education": [
        ("Online Course - Udemy", 800, 2500),
        ("Book Purchase - Amazon", 400, 1200),
        ("Tuition Fee Payment", 5000, 15000),
        ("Educational Software", 1200, 3000),
        ("Skill Development Course", 2500, 8000)
    ],
    
    "Home & Garden": [
        ("Monthly Rent Payment", 25000, 50000),
        ("Home Maintenance", 1500, 5000),
        ("Furniture Purchase - IKEA", 8000, 25000),
        ("Home Appliances", 12000, 35000),
        ("Garden Plants & Tools", 300, 1000),
        ("Home Decor Items", 1200, 4000)
    ],
    
    "Personal Care": [
        ("Salon Visit", 400, 1200),
        ("Gym Membership", 1500, 3000),
        ("Cosmetics Purchase", 600, 2000),
        ("Spa Treatment", 2000, 5000),
        ("Barber Shop", 100, 300),
        ("Fitness Equipment", 3000, 10000)
    ],
    
    "Bills & Finance": [
        ("Credit Card Payment", 5000, 25000),
        ("Personal Loan EMI", 8000, 15000),
        ("Bank Charges", 50, 300),
        ("Insurance Premium", 3000, 12000),
        ("Income Tax Payment", 15000, 50000),
        ("Mutual Fund SIP", 5000, 20000)
    ],
    
    "Investments": [
        ("Mutual Fund Investment", 10000, 50000),
        ("Stock Purchase", 5000, 25000),
        ("SIP Contribution", 3000, 10000),
        ("Gold Investment", 15000, 50000),
        ("Fixed Deposit", 50000, 200000)
    ],
    
    "Subscriptions": [
        ("Amazon Prime", 129, 1499),
        ("YouTube Premium", 129, 189),
        ("Disney+ Hotstar", 299, 1499),
        ("Microsoft Office 365", 489, 6199),
        ("Adobe Creative Suite", 1675, 4000)
    ],
    
    "Gifts & Donations": [
        ("Gift Purchase", 500, 5000),
        ("Charitable Donation", 1000, 10000),
        ("Birthday Gift", 800, 3000),
        ("Wedding Gift", 2000, 15000)
    ],
    
    "Sports & Fitness": [
        ("Sports Equipment", 1000, 5000),
        ("Fitness Class", 500, 2000),
        ("Yoga Session", 300, 800),
        ("Swimming Pool Fee", 200, 600)
    ],
    
    "Business": [
        ("Office Supplies", 800, 3000),
        ("Client Meeting Expense", 1200, 4000),
        ("Business Travel", 2500, 8000),
        ("Vendor Payment", 10000, 50000)
    ],
    
    "Income": [
        ("Salary Credit", 50000, 150000),
        ("Freelance Payment", 15000, 50000),
        ("Bonus Payment", 25000, 100000),
        ("Investment Return", 5000, 25000),
        ("Refund Credit", 500, 5000),
        ("Interest Received", 1000, 5000),
        ("Dividend Credit", 2000, 15000)
    ],
    
    "ATM/Cash": [
        ("ATM Cash Withdrawal", 2000, 10000),
        ("Bank Cash Withdrawal", 5000, 20000)
    ],
    
    "Transfer": [
        ("UPI Transfer to Friend", 500, 5000),
        ("NEFT Transfer", 10000, 50000),
        ("Family Transfer", 5000, 25000),
        ("Loan Transfer", 15000, 50000)
    ]
}

# Income sources for credit transactions
income_sources = [
    ("Salary - ABC Tech Solutions", 75000, 85000),
    ("Freelance Project Payment", 25000, 45000),
    ("Investment Dividend", 3000, 8000),
    ("Fixed Deposit Interest", 1500, 3000),
    ("Cashback Credit", 200, 800),
    ("Refund - Online Purchase", 500, 2000),
    ("Bonus Payment", 15000, 35000),
    ("Rental Income", 20000, 30000)
]

def generate_transactions():
    transactions = []
    current_date = start_date
    
    # Ensure regular income (salary on 1st of each month)
    for month in range(3):  # 3 months
        salary_date = datetime(2024, 11 + month, 1) if month < 2 else datetime(2025, 1, 1)
        if salary_date <= end_date:
            transactions.append({
                'Date': salary_date.strftime('%d %b %Y'),
                'Details': 'Salary Credit - ABC Tech Solutions',
                'Amount': random.uniform(75000, 85000),
                'Debit/Credit': 'Credit'
            })
    
    # Add other income transactions
    for _ in range(15):  # Additional income transactions
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        detail, min_amt, max_amt = random.choice(income_sources)
        transactions.append({
            'Date': date.strftime('%d %b %Y'),
            'Details': detail,
            'Amount': round(random.uniform(min_amt, max_amt), 2),
            'Debit/Credit': 'Credit'
        })
    
    # Generate expense transactions with realistic patterns
    for category, templates in transaction_templates.items():
        if category == "Income":  # Skip income category for expenses
            continue
            
        # Determine frequency based on category
        if category in ["Food & Dining"]:
            num_transactions = random.randint(25, 40)  # High frequency
        elif category in ["Groceries", "Transportation", "Utilities"]:
            num_transactions = random.randint(15, 25)  # Medium frequency
        elif category in ["Shopping", "Entertainment", "Personal Care"]:
            num_transactions = random.randint(8, 15)   # Medium-low frequency
        elif category in ["Travel", "Home & Garden", "Bills & Finance"]:
            num_transactions = random.randint(3, 8)    # Low frequency
        else:
            num_transactions = random.randint(5, 12)   # Default frequency
        
        for _ in range(num_transactions):
            date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            detail, min_amt, max_amt = random.choice(templates)
            
            # Add some variation to amounts to create anomalies
            amount = random.uniform(min_amt, max_amt)
            
            # 5% chance of creating an anomaly (unusually high amount)
            if random.random() < 0.05:
                amount *= random.uniform(2.5, 4.0)  # Create high anomaly
            # 3% chance of creating low anomaly
            elif random.random() < 0.03:
                amount *= random.uniform(0.1, 0.3)  # Create low anomaly
            
            transactions.append({
                'Date': date.strftime('%d %b %Y'),
                'Details': detail,
                'Amount': round(amount, 2),
                'Debit/Credit': 'Debit'
            })
    
    # Sort transactions by date
    transactions.sort(key=lambda x: datetime.strptime(x['Date'], '%d %b %Y'))
    
    return transactions

# Generate the dataset
sample_data = generate_transactions()
df = pd.DataFrame(sample_data)

# Save to CSV
df.to_csv('finwise_sample_data_3months.csv', index=False)

print(f"Generated {len(df)} transactions")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Total Credits: ₹{df[df['Debit/Credit'] == 'Credit']['Amount'].sum():,.2f}")
print(f"Total Debits: ₹{df[df['Debit/Credit'] == 'Debit']['Amount'].sum():,.2f}")
print(f"Net Flow: ₹{(df[df['Debit/Credit'] == 'Credit']['Amount'].sum() - df[df['Debit/Credit'] == 'Debit']['Amount'].sum()):,.2f}")
print("\nSample transactions:")
print(df.head(10).to_string(index=False))

# Display category distribution
debit_df = df[df['Debit/Credit'] == 'Debit'].copy()

# Add category mapping for analysis
def categorize_sample_transaction(details):
    details_lower = str(details).lower()
    
    category_keywords = {
        "Food & Dining": ["swiggy", "zomato", "kfc", "mcdonalds", "cafe", "restaurant", "pizza", "subway", "dhaba", "starbucks", "domino", "haldiram"],
        "Groceries": ["reliance fresh", "dmart", "bigbasket", "kirana", "zepto", "spencer", "supermarket", "grocery", "fruits", "vegetables"],
        "Transportation": ["uber", "ola", "petrol", "diesel", "metro", "auto", "bus", "rapido", "gas station"],
        "Shopping": ["amazon", "flipkart", "myntra", "zara", "h&m", "electronics", "nike", "adidas", "lifestyle"],
        "Utilities": ["electricity", "water bill", "jio", "airtel", "gas cylinder", "broadband", "dth"],
        "Healthcare": ["apollo", "pharmacy", "doctor", "hospital", "dental", "medicine", "health", "checkup"],
        "Entertainment": ["netflix", "bookmyshow", "spotify", "cinema", "gaming", "concert", "prime"],
        "Travel": ["indigo", "flight", "hotel", "oyo", "makemytrip", "railway", "goibibo", "agoda"],
        "Education": ["course", "udemy", "book", "tuition", "educational", "skill"],
        "Home & Garden": ["rent", "maintenance", "ikea", "furniture", "appliances", "garden", "home"],
        "Personal Care": ["salon", "gym", "cosmetics", "spa", "barber", "fitness"],
        "Bills & Finance": ["credit card", "loan", "emi", "bank", "insurance", "tax", "mutual fund"],
        "Investments": ["investment", "stock", "sip", "gold", "fixed deposit"],
        "Subscriptions": ["prime", "youtube", "disney", "microsoft", "adobe"],
        "Gifts & Donations": ["gift", "donation", "birthday", "wedding"],
        "Sports & Fitness": ["sports", "fitness", "yoga", "swimming"],
        "Business": ["office", "client", "business", "vendor"],
        "ATM/Cash": ["atm", "cash withdrawal"],
        "Transfer": ["transfer", "upi", "neft", "family", "friend"]
    }
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in details_lower:
                return category
    return "Other"

if not debit_df.empty:
    debit_df['Category'] = debit_df['Details'].apply(categorize_sample_transaction)
    category_summary = debit_df.groupby('Category')['Amount'].agg(['count', 'sum']).round(2)
    category_summary.columns = ['Count', 'Total Amount']
    category_summary = category_summary.sort_values('Total Amount', ascending=False)
    print(f"\nCategory-wise Expense Summary:")
    print(category_summary.to_string())

print(f"\n✅ Sample data saved as 'finwise_sample_data_3months.csv'")
print(f"📊 This dataset includes:")
print(f"   • Regular monthly salaries and varied income sources")
print(f"   • Realistic spending patterns across all categories")
print(f"   • Built-in anomalies for testing anomaly detection")
print(f"   • Seasonal variations and weekend/weekday patterns")
print(f"   • Mix of small daily expenses and large occasional purchases")