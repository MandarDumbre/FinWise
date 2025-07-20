⚡ FinWise - Smart Expense Tracking Dashboard
A powerful, intelligent financial management tool built with Streamlit that provides automated transaction categorization, budget tracking, anomaly detection, and comprehensive financial insights.

🚀 Features
📊 Smart Categorization: Regex-based automatic transaction categorization using predefined rules
💰 Budget Tracking: Set and monitor monthly spending goals across categories
🚨 Anomaly Detection: Statistical analysis to flag unusual spending patterns
📈 Advanced Analytics: Interactive visualizations and trend analysis
🔍 Dynamic Filtering: Filter transactions by date range and categories
💡 Smart Insights: AI-powered financial insights and recommendations
📱 Responsive Design: Modern, mobile-friendly interface
📥 Data Export: Download filtered transaction data
🛠️ Technology Stack
Frontend: Streamlit
Data Processing: Pandas, NumPy
Visualizations: Plotly
Styling: Custom CSS with gradient themes
Data Format: CSV files
📋 Prerequisites
Python 3.8 or higher
pip package manager
🚀 Installation
Clone the repository
bash
git clone https://github.com/MandarDumbre/finwise.git
cd finwise
Create a virtual environment (recommended)
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
bash
pip install -r requirements.txt
Create the categorization rules file Create a categories.json file in the project root with your categorization rules:
json
{
  "Food & Dining": ["swiggy", "zomato", "restaurant", "cafe", "food"],
  "Transportation": ["uber", "ola", "petrol", "metro", "taxi"],
  "Shopping": ["amazon", "flipkart", "mall", "shopping"],
  "Utilities": ["electricity", "water", "gas", "internet"],
  "Healthcare": ["hospital", "pharmacy", "doctor", "medicine"],
  "Entertainment": ["netflix", "movie", "cinema", "gaming"],
  "Income": ["salary", "bonus", "dividend", "interest"]
}
Run the application
bash
streamlit run finwise.py
📊 Data Format
Your CSV file should contain the following columns:

Column	Format	Description
Date	DD Mon YYYY	Transaction date (e.g., "15 Jan 2024")
Details	Text	Transaction description
Amount	Number	Transaction amount (without currency symbols)
Debit/Credit	Text	Either "Debit" or "Credit"
Sample Data Structure
csv
Date,Details,Amount,Debit/Credit
15 Jan 2024,Swiggy Order - Pizza,450.00,Debit
16 Jan 2024,Salary Credit,75000.00,Credit
17 Jan 2024,Uber Ride,120.50,Debit
🎯 Usage Guide
1. Upload Transaction Data
Click "📁 Upload your transaction CSV file"
Select your properly formatted CSV file
The system will automatically validate and process your data
2. Set Budget Goals
Use the sidebar to set monthly budget limits for different categories
Track your spending against these goals in real-time
3. Explore Analytics
Navigate through different tabs:

💸 Expenses: Detailed expense analysis and category breakdown
💰 Income: Income tracking and analysis
📊 Analytics: Interactive charts and visualizations
📈 Insights: AI-powered financial insights
🚨 Anomalies: Detection of unusual spending patterns
4. Filter and Export
Use date range and category filters to focus on specific data
Export filtered results for further analysis
📁 Project Structure
finwise/
├── finwise.py                 # Main application file
├── data_generator.py          # Sample data generation script
├── categories.json           # Categorization rules (create this)
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── sample_data/             # Directory for sample datasets
🧪 Sample Data Generation
The project includes a data generator script to create realistic sample data for testing:

bash
python data_generator.py
This will generate finwise_sample_data_3months.csv with:

3 months of realistic transaction data
Multiple categories with varied spending patterns
Built-in anomalies for testing detection algorithms
Regular income sources and varied expenses
🔧 Customization
Adding New Categories
Edit categories.json to add new categories or modify existing rules:

json
{
  "Your Category": ["keyword1", "keyword2", "regex_pattern"]
}
Adjusting Anomaly Detection
Modify the threshold_zscore parameter in the detect_anomalies() function:

Lower values (1.5-2.0): More sensitive, detects smaller anomalies
Higher values (2.5-3.0): Less sensitive, only major anomalies
📈 Analytics Features
Visualizations
Daily Spending Trends: Line chart showing spending patterns over time
Category Distribution: Pie chart of expense breakdown
Top Categories: Bar chart of highest spending areas
Insights Engine
Overall financial health summary
Spending habit analysis
Budget adherence tracking
Anomaly explanations
Behavioral pattern recognition
🛡️ Security & Privacy
Local Processing: All data processing happens locally on your machine
No Data Storage: The application doesn't store your financial data
Session-based: Data exists only during your browser session
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Development Setup
Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🐛 Known Issues
Large datasets (>10,000 transactions) may experience slower loading times
Date parsing requires specific formats (DD Mon YYYY or YYYY-MM-DD)
🔮 Roadmap
 Multi-currency support
 Advanced ML-based categorization
 Export to PDF reports
 Mobile app version
 Bank API integrations
 Goal-based savings tracking
📞 Support
If you encounter any issues or have questions:

Check the Issues section
Create a new issue with detailed information
Provide sample data (anonymized) if possible
🙏 Acknowledgments
Built with Streamlit
Visualizations powered by Plotly
Data processing with Pandas
<div align="center">
⚡ FinWise - Making Financial Management Smart and Simple ⚡

⭐ Star this repo | 🐛 Report Bug | ✨ Request Feature


