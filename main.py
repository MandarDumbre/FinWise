import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import re # Import regex module
import numpy as np # For numerical operations like standard deviation

import json

# --- Load Keyword-Based Categorization Rules from JSON ---
with open("categories.json", "r", encoding="utf-8") as f:
    CATEGORY_RULES = json.load(f)
def load_json(file_path):
    """    Load a JSON file and return its content.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
# --- Load Keyword-Based Categorization Rules ---
def categorize_transaction_by_keywords(details, amount, debit_credit):
    """
    Categorizes a financial transaction based on predefined regex keywords.
    """
    details_lower = str(details).lower()

    if debit_credit == "Credit":
        # Check for specific income keywords first
        for category, patterns in CATEGORY_RULES.items():
            if category == "Income":
                for pattern in patterns:
                    if re.search(pattern, details_lower):
                        return "Income"
        return "Income" # Default to Income for any credit not caught by explicit income keywords

    # For Debit transactions
    for category, patterns in CATEGORY_RULES.items():
        if category == "Income": # Skip "Income" category for debit transactions
            continue
        for pattern in patterns:
            if re.search(pattern, details_lower):
                return category
    return "Other" # Default if no keyword matches for debits

def detect_anomalies(df, category_col="Category", amount_col="Amount", threshold_zscore=2.5):
    """
    Detects anomalies in spending based on Z-score within each category.
    A higher Z-score threshold means fewer, more extreme anomalies.
    """
    if df.empty:
        return pd.DataFrame()

    anomalies_list = []
    # Only consider debit transactions for anomaly detection
    debit_transactions = df[df["Debit/Credit"] == "Debit"].copy()

    if debit_transactions.empty:
        return pd.DataFrame()

    # Ensure 'Date' column is datetime before using .dt accessor
    debit_transactions['Date'] = pd.to_datetime(debit_transactions['Date'])

    # Calculate mean and std dev of amounts for each category
    category_stats = debit_transactions.groupby(category_col)[amount_col].agg(['mean', 'std']).reset_index()
    category_stats.rename(columns={'mean': 'CategoryMean', 'std': 'CategoryStd'}, inplace=True)

    # Merge stats back to the transactions
    debit_transactions = pd.merge(debit_transactions, category_stats, on=category_col, how='left')

    # Calculate Z-score for each transaction
    # Handle cases where std dev is 0 (e.g., all transactions in a category are the same amount)
    debit_transactions['ZScore'] = debit_transactions.apply(
        lambda row: (row[amount_col] - row['CategoryMean']) / row['CategoryStd']
        if row['CategoryStd'] > 0 else np.nan, axis=1
    )

    # Flag anomalies based on threshold
    # We are looking for unusually high expenses, so Z-score > threshold
    anomalies_df = debit_transactions[debit_transactions['ZScore'].abs() > threshold_zscore].copy()
    anomalies_df['Anomaly_Reason'] = anomalies_df.apply(
        lambda row: f"Unusually high expense (Z-score: {row['ZScore']:.2f})" if row['ZScore'] > 0 else f"Unusually low expense (Z-score: {row['ZScore']:.2f})",
        axis=1
    )
    return anomalies_df[['Date', 'Details', 'Amount', category_col, 'Anomaly_Reason', 'ZScore']]


# Page Configuration
st.set_page_config(
    page_title=" FinWise ",
    page_icon="⚡💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1A237E 0%, #283593 100%); /* Deep Blue */
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #FF6F00 0%, #FFB300 100%); /* Orange-Amber */
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .category-card {
        background: linear-gradient(135deg, #00897B 0%, #00BFA5 100%); /* Teal */
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1A237E 0%, #283593 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .success-message {
        background-color: #E8F5E9; /* Light Green */
        color: #1B5E20; /* Dark Green */
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50; /* Green border */
        margin: 1rem 0;
    }
    .advanced-badge {
        background: linear-gradient(90deg, #880E4F 0%, #C2185B 100%); /* Dark Pink */
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .anomaly-highlight {
        background-color: #FFEBEE; /* Light Red */
        color: #B71C1C; /* Dark Red */
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data and flags
if "processed_transactions" not in st.session_state:
    st.session_state.processed_transactions = None
if "categorization_complete" not in st.session_state:
    st.session_state.categorization_complete = False
if "budget_goals" not in st.session_state:
    st.session_state.budget_goals = {} # Stores user-defined budget goals

def process_transactions_advanced(df):
    """Process all transactions with advanced keyword categorization."""
    if df is None or df.empty:
        return df

    df["Category"] = "Other" # Initialize column
    df["Category"] = df.apply(
        lambda row: categorize_transaction_by_keywords(row["Details"], row["Amount"], row["Debit/Credit"]),
        axis=1
    )
    return df

def load_and_process_file(file):
    """Load and process the uploaded CSV file with improved validation."""
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]

        # Validate and convert 'Amount'
        if "Amount" in df.columns:
            df["Amount"] = df["Amount"].astype(str).str.replace(",", "").str.replace("₹", "")
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            if df["Amount"].isnull().any():
                st.warning("Some 'Amount' values could not be converted to numbers and were set to NaN. These rows will be dropped.")
            df = df.dropna(subset=["Amount"])
        else:
            st.error("Missing required column: 'Amount'. Please ensure your CSV has this column.")
            return None

        # Validate and convert 'Date'
        if "Date" in df.columns:
            try:
                df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
            except ValueError:
                try:
                    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
                except ValueError:
                    st.error("Could not parse 'Date' column. Please ensure it's in 'DD Mon YYYY' or 'YYYY-MM-DD' format.")
                    return None
            if df["Date"].isnull().any():
                st.warning("Some 'Date' values could not be parsed and were set to NaT. These rows will be dropped.")
            df = df.dropna(subset=["Date"])
        else:
            st.error("Missing required column: 'Date'. Please ensure your CSV has this column.")
            return None

        # Validate 'Debit/Credit'
        if "Debit/Credit" not in df.columns:
            st.error("Missing required column: 'Debit/Credit'. Please ensure your CSV has this column.")
            return None
        # Ensure 'Debit/Credit' column only contains 'Debit' or 'Credit'
        df['Debit/Credit'] = df['Debit/Credit'].astype(str).str.strip()
        invalid_dc = df[~df['Debit/Credit'].isin(['Debit', 'Credit'])]
        if not invalid_dc.empty:
            st.warning(f"Found {len(invalid_dc)} rows with invalid 'Debit/Credit' values (expected 'Debit' or 'Credit'). These rows will be dropped.")
            df = df[df['Debit/Credit'].isin(['Debit', 'Credit'])]


        required_cols = ["Date", "Details", "Amount", "Debit/Credit"]
        # Final check for any missing required columns after initial processing
        for col in required_cols:
            if col not in df.columns or df[col].isnull().all():
                st.error(f"Critical column '{col}' is missing or entirely empty after initial processing. Cannot proceed.")
                return None

        df = df.dropna(subset=required_cols) # Final dropna for any remaining NaNs in critical cols
        if df.empty:
            st.warning("No valid transactions remaining after cleaning. Please check your CSV data.")
            return None

        return df

    except Exception as e:
        st.error(f"Error processing file: {str(e)}. Please ensure it's a valid CSV with expected columns and data types.")
        return None

def create_enhanced_visualizations(df):
    """Create enhanced visualizations"""
    if df is None or df.empty:
        st.info("No data available for visualizations.")
        return None, None, None

    df['Date'] = pd.to_datetime(df['Date'])

    # Changed from Month to Day for daily spending trend
    df["Day"] = df["Date"].dt.to_period("D")
    daily_spending = df.groupby("Day")["Amount"].sum().reset_index()
    daily_spending["Day"] = daily_spending["Day"].astype(str)

    fig_trend = px.line(
        daily_spending, # Changed to daily_spending
        x="Day", # Changed to Day
        y="Amount",
        title="📈 Daily Spending Trend", # Changed title
        color_discrete_sequence=["#1A237E"] # Match header gradient
    )
    fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            xaxis_title="Day", yaxis_title="Amount (₹)") # Changed x-axis title

    expenses_df = df[df["Debit/Credit"] == "Debit"].copy()
    fig_pie = None
    fig_bar = None

    if not expenses_df.empty:
        category_totals = expenses_df.groupby("Category")["Amount"].sum().reset_index()
        category_totals = category_totals.sort_values("Amount", ascending=False)

        fig_pie = px.pie(
            category_totals,
            values="Amount",
            names="Category",
            title="🎯 Expense Distribution by Category",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        top_categories = category_totals.head(10)
        fig_bar = px.bar(
            top_categories,
            x="Category",
            y="Amount",
            title="💰 Top Spending Categories",
            color="Amount",
            color_continuous_scale="Viridis"
        )
        fig_bar.update_layout(xaxis_tickangle=-45, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              xaxis_title="Category", yaxis_title="Total Amount (₹)")
    else:
        st.info("No expense transactions found for category analysis charts.")

    return fig_trend, fig_pie, fig_bar


def generate_smart_insights(df_processed, budget_goals):
    """Generates textual insights based on processed financial data, including budget adherence and anomalies."""
    insights = []

    # Overall Metrics
    total_debits = df_processed[df_processed["Debit/Credit"] == "Debit"]["Amount"].sum()
    total_credits = df_processed[df_processed["Debit/Credit"] == "Credit"]["Amount"].sum()
    net_flow = total_credits - total_debits

    insights.append(f"**Overall Financial Snapshot:**")
    insights.append(f"- Your total expenses amount to **₹{total_debits:,.2f}**.")
    insights.append(f"- Your total income/credits amount to **₹{total_credits:,.2f}**.")
    insights.append(f"- Your net financial flow is **₹{net_flow:,.2f}**.")

    debits_df = df_processed[df_processed["Debit/Credit"] == "Debit"].copy()

    if not debits_df.empty:
        # Ensure 'Date' column is datetime before using .dt accessor on debits_df
        debits_df['Date'] = pd.to_datetime(debits_df['Date'])
        
        # Spending Habits
        category_summary = debits_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        if not category_summary.empty:
            top_category = category_summary.index[0]
            top_category_amount = category_summary.iloc[0]
            insights.append(f"\n**Spending Habits:**")
            insights.append(f"- Your largest spending area is **{top_category}**, accounting for **₹{top_category_amount:,.2f}**.")
            if len(category_summary) > 1:
                other_top_categories = category_summary.head(3).drop(top_category, errors='ignore')
                if not other_top_categories.empty:
                    insights.append(f"- Other significant expenses include: {', '.join([f'{cat} (₹{amt:,.2f})' for cat, amt in other_top_categories.items()])}.")
        else:
            insights.append("No categorized expenses to analyze spending habits.")

        avg_transaction_debit = debits_df["Amount"].mean()
        insights.append(f"- The average amount per expense transaction is **₹{avg_transaction_debit:,.2f}**.")

        # Budget Adherence (for the current month/period of data)
        insights.append(f"\n**Budget Adherence:**")
        current_month_data = debits_df[debits_df['Date'].dt.to_period('M') == debits_df['Date'].dt.to_period('M').max()]
        if not current_month_data.empty and budget_goals:
            current_month_spending = current_month_data.groupby('Category')['Amount'].sum()
            budget_insights = []
            for category, budget_amount in budget_goals.items():
                spent = current_month_spending.get(category, 0)
                if budget_amount > 0:
                    if spent > budget_amount:
                        budget_insights.append(f"- You've **exceeded** your {category} budget (₹{budget_amount:,.2f}) by ₹{(spent - budget_amount):,.2f}.")
                    else:
                        remaining = budget_amount - spent
                        budget_insights.append(f"- You have **₹{remaining:,.2f}** remaining in your {category} budget (out of ₹{budget_amount:,.2f}).")
            if budget_insights:
                insights.extend(budget_insights)
            else:
                insights.append("- No active budget goals for the current month's categories.")
        else:
            insights.append("- No budget goals set or no data for the current period.")


        # Anomaly Detection Insights
        anomalies_df = detect_anomalies(df_processed) # Use df_processed to get anomalies across all data
        if not anomalies_df.empty:
            insights.append(f"\n**Anomaly Detection:**")
            insights.append(f"- Detected **{len(anomalies_df)} potential anomalies** in your spending.")
            for i, row in anomalies_df.head(3).iterrows(): # Show top 3 anomalies
                insights.append(f"  - On {row['Date'].strftime('%Y-%m-%d')}, a **₹{row['Amount']:,.2f}** transaction for '{row['Details']}' in '{row['Category']}' was flagged as: {row['Anomaly_Reason']}.")
            if len(anomalies_df) > 3:
                insights.append(f"  - (And {len(anomalies_df) - 3} more anomalies...)")
        else:
            insights.append(f"\n**Anomaly Detection:**")
            insights.append("- No significant spending anomalies detected.")


        # Time-based insights (e.g., busiest spending days/months)
        # FIX: Ensure 'DayOfWeek' and 'MonthYear' are created on debits_df itself
        debits_df['DayOfWeek'] = debits_df['Date'].dt.day_name()
        spending_by_day = debits_df.groupby('DayOfWeek')['Amount'].sum().sort_values(ascending=False)
        if not spending_by_day.empty:
            busiest_day = spending_by_day.index[0]
            insights.append(f"\n**Behavioral Insights:**")
            insights.append(f"- You tend to spend most on **{busiest_day}s**.")

        debits_df['MonthYear'] = debits_df['Date'].dt.to_period('M')
        monthly_trends = debits_df.groupby('MonthYear')['Amount'].sum()
        if len(monthly_trends) > 1:
            latest_month = monthly_trends.index[-1]
            previous_month = monthly_trends.index[-2]
            if previous_month:
                change = monthly_trends[latest_month] - monthly_trends[previous_month]
                if change > 0:
                    insights.append(f"- Your spending in {latest_month.strftime('%B %Y')} increased by **₹{change:,.2f}** compared to {previous_month.strftime('%B %Y')}.")
                elif change < 0:
                    insights.append(f"- Your spending in {latest_month.strftime('%B %Y')} decreased by **₹{-change:,.2f}** compared to {previous_month.strftime('%B %Y')}.")
                else:
                    insights.append(f"- Your spending remained consistent in {latest_month.strftime('%B %Y')} compared to {previous_month.strftime('%B %Y')}.")

    else:
        insights.append("No debit transactions found to generate detailed spending insights.")

    return "\n".join(insights)


def main():
    st.markdown("""
    <div class="main-header">
        <h1>⚡ FinWise  </h1>
        <p>Smart expense tracking with rule-based categorization & insights</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🚀 Features")
        st.markdown("""
        - **Regex Categorization**: Flexible and robust rule-based categorization.
        - **Budget Tracking**: Set and monitor spending goals.
        - **Anomaly Detection**: Flag unusual transactions for review.
        - **Dynamic Filters**: Explore your data by date and category.
        - **Enhanced Insights**: Comprehensive textual summaries.
        """)

        st.markdown("### 📊 Quick Stats")
        if st.session_state.processed_transactions is not None:
            df_sidebar = st.session_state.processed_transactions
            debits_sidebar = df_sidebar[df_sidebar["Debit/Credit"] == "Debit"].copy()
            credits_sidebar = df_sidebar[df_sidebar["Debit/Credit"] == "Credit"].copy()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="metric-card"><h3>Total Expenses</h3><h2>₹{debits_sidebar["Amount"].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h3>Total Income</h3><h2>₹{credits_sidebar["Amount"].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            st.metric("Transactions (Debit)", len(debits_sidebar))
            st.metric("Categories (Debit)", debits_sidebar["Category"].nunique())
            # FIX: Changed outer f-string quotes to single quotes to avoid conflict with inner double quotes
            st.metric("Net Flow", f'₹{(credits_sidebar["Amount"].sum() - debits_sidebar["Amount"].sum()):,.2f}')

        st.markdown("---")
        st.markdown("### 🎯 Set Monthly Budgets")
        # Get all unique categories from processed data for budget setting
        if st.session_state.processed_transactions is not None:
            all_expense_categories = sorted(st.session_state.processed_transactions[st.session_state.processed_transactions["Debit/Credit"] == "Debit"]["Category"].unique())
            if "Other" in all_expense_categories: # Move 'Other' to end for better UX
                all_expense_categories.remove("Other")
                all_expense_categories.append("Other")

            for category in all_expense_categories:
                # Use a unique key for each number_input to prevent re-rendering issues
                st.session_state.budget_goals[category] = st.number_input(
                    f"Budget for {category} (₹)",
                    min_value=0.0,
                    value=st.session_state.budget_goals.get(category, 0.0),
                    step=100.0,
                    key=f"budget_{category}"
                )
            if st.button("Clear All Budgets", key="clear_budgets"):
                st.session_state.budget_goals = {cat: 0.0 for cat in all_expense_categories}
                st.rerun() # Rerun to update budget inputs

    # Main content area
    uploaded_file = st.file_uploader(
        "📁 Upload your transaction CSV file",
        type=["csv"],
        help="Upload a CSV file with columns: Date (DD Mon YYYY), Details, Amount, Debit/Credit"
    )

    if uploaded_file is not None:
        with st.spinner("Loading & Validating transaction data..."):
            df = load_and_process_file(uploaded_file)

        if df is not None:
            st.success(f"✅ Loaded {len(df)} transactions successfully!")

            with st.spinner("Categorizing transactions..."):
                df_processed = process_transactions_advanced(df.copy())
                st.session_state.processed_transactions = df_processed
                st.session_state.categorization_complete = True

            if st.session_state.categorization_complete and st.session_state.processed_transactions is not None:
                df_current = st.session_state.processed_transactions.copy() # Work on a copy for filtering

                st.markdown("### 🔍 Filter Transactions")
                col_date_start, col_date_end, col_category_filter = st.columns([1, 1, 2])

                min_date = df_current['Date'].min().date() if not df_current.empty else datetime.now().date() - timedelta(days=365)
                max_date = df_current['Date'].max().date() if not df_current.empty else datetime.now().date()

                with col_date_start:
                    start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
                with col_date_end:
                    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

                # Get all unique categories for filtering
                all_filterable_categories = sorted(df_current["Category"].unique().tolist())
                if "Other" in all_filterable_categories:
                    all_filterable_categories.remove("Other")
                    all_filterable_categories.append("Other") # Move to end

                with col_category_filter:
                    selected_categories = st.multiselect(
                        "Filter by Category",
                        options=all_filterable_categories,
                        default=all_filterable_categories # Default to all selected
                    )

                # Apply filters
                filtered_df = df_current[
                    (df_current['Date'].dt.date >= start_date) &
                    (df_current['Date'].dt.date <= end_date) &
                    (df_current['Category'].isin(selected_categories))
                ].copy() # Ensure a copy after filtering

                if filtered_df.empty:
                    st.warning("No transactions match the selected filters.")
                else:
                    st.markdown(f"**Displaying {len(filtered_df)} transactions after filtering.**")

                tab1, tab2, tab3, tab4, tab5 = st.tabs(["💸 Expenses", "💰 Income", "📊 Analytics", "📈 Insights", "🚨 Anomalies"])

                with tab1:
                    st.markdown("### 💸 Expense Analysis")
                    debits_df = filtered_df[filtered_df["Debit/Credit"] == "Debit"].copy()

                    if not debits_df.empty:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f'<div class="metric-card"><h3>Total Expenses</h3><h2>₹{debits_df["Amount"].sum():,.0f}</h2></div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f'<div class="metric-card"><h3>Transactions</h3><h2>{len(debits_df)}</h2></div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown(f'<div class="metric-card"><h3>Avg. Amount</h3><h2>₹{debits_df["Amount"].mean():,.0f}</h2></div>', unsafe_allow_html=True)
                        with col4:
                            st.markdown(f'<div class="metric-card"><h3>Categories</h3><h2>{debits_df["Category"].nunique()}</h2></div>', unsafe_allow_html=True)

                        st.markdown("---")
                        st.markdown("### 📝 Review & Edit Categories")
                        all_editable_categories = sorted(list(set(CATEGORY_RULES.keys()).union(set(debits_df["Category"].unique()))))
                        if "Income" in all_editable_categories:
                            all_editable_categories.remove("Income")
                        if "Other" not in all_editable_categories:
                            all_editable_categories.append("Other")
                        all_editable_categories = sorted(all_editable_categories)

                        edited_df = st.data_editor(
                            debits_df[["Date", "Details", "Amount", "Category"]].head(50), # Show first 50 for editing
                            column_config={
                                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                                "Amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
                                "Category": st.column_config.SelectboxColumn("Category", options=all_editable_categories, help="Rule-based category")
                            },
                            hide_index=True,
                            use_container_width=True,
                            key="expense_editor"
                        )
                        # Note: Edits made in st.data_editor are not automatically saved back to the main DataFrame
                        # For persistence of edits, you would need to implement logic to update st.session_state.processed_transactions
                        # based on the changes in 'edited_df'.

                        st.markdown("### 📊 Category Breakdown")
                        category_summary = debits_df.groupby("Category").agg({"Amount": ["sum", "count", "mean"]}).round(2)
                        category_summary.columns = ["Total Amount", "Count", "Average"]
                        category_summary = category_summary.sort_values("Total Amount", ascending=False)
                        st.dataframe(
                            category_summary,
                            use_container_width=True,
                            column_config={
                                "Total Amount": st.column_config.NumberColumn("Total Amount", format="₹%.2f"),
                                "Average": st.column_config.NumberColumn("Average", format="₹%.2f")
                            }
                        )
                    else:
                        st.info("No debit transactions found to analyze expenses based on current filters.")


                with tab2:
                    st.markdown("### 💰 Income Analysis")
                    credits_df = filtered_df[filtered_df["Debit/Credit"] == "Credit"].copy()
                    if not credits_df.empty:
                        total_income = credits_df["Amount"].sum()
                        st.metric("💰 Total Income", f"₹{total_income:,.2f}")
                        st.dataframe(
                            credits_df[["Date", "Details", "Amount", "Category"]],
                            use_container_width=True,
                            column_config={
                                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                                "Amount": st.column_config.NumberColumn("Amount", format="₹%.2f")
                            }
                        )
                    else:
                        st.info("No credit transactions found based on current filters.")

                with tab3:
                    st.markdown("### 📊 Advanced Analytics")
                    debits_df_for_charts = filtered_df[filtered_df["Debit/Credit"] == "Debit"].copy()
                    if not debits_df_for_charts.empty:
                        fig_trend, fig_pie, fig_bar = create_enhanced_visualizations(debits_df_for_charts)
                        if fig_trend:
                            st.plotly_chart(fig_trend, use_container_width=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            if fig_pie:
                                st.plotly_chart(fig_pie, use_container_width=True)
                            else:
                                st.info("Not enough data to generate Expense Distribution Pie Chart.")
                        with col2:
                            if fig_bar:
                                st.plotly_chart(fig_bar, use_container_width=True)
                            else:
                                st.info("Not enough data to generate Top Spending Categories Bar Chart.")
                    else:
                        st.info("No debit transactions found for advanced analytics charts based on current filters.")


                with tab4:
                    st.markdown("### 📈 Smart Insights")
                    if not filtered_df.empty:
                        insights_text = generate_smart_insights(filtered_df.copy(), st.session_state.budget_goals)
                        st.markdown(insights_text)
                    else:
                        st.info("Apply filters to see smart insights for the selected period/categories.")

                with tab5:
                    st.markdown("### 🚨 Anomalous Transactions")
                    anomalies_in_filtered_data = detect_anomalies(filtered_df.copy())
                    if not anomalies_in_filtered_data.empty:
                        st.warning(f"Found {len(anomalies_in_filtered_data)} potential anomalies in the filtered data:")
                        st.dataframe(
                            anomalies_in_filtered_data.drop(columns=['ZScore']),
                            use_container_width=True,
                            column_config={
                                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                                "Amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
                            }
                        )
                        st.markdown("""
                            <div class="anomaly-highlight">
                                Note: Anomalies are detected based on statistical deviation within categories.
                                Review these transactions for potential errors or unusual spending.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No significant spending anomalies detected in the filtered data.")


                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Filtered Data",
                        data=csv_data,
                        file_name=f"filtered_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 Advanced Analytics | Built with Streamlit</p>
        <p><span class="advanced-badge">Data-Driven</span> Finance Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()