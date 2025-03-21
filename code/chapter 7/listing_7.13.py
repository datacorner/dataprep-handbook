import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("../data/superstore/samplesuperstore.csv", encoding='UTF8')

    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

    # Group by Customer ID to get unique customer metrics
    customer_orders = df.groupby('Customer ID').agg({
        'Order ID': 'count',           # Total number of orders
        'Sales': 'sum',                # Total sales per customer
        'Profit': 'sum',               # Total profit per customer
        'Order Date': ['min', 'max']   # First and last purchase dates
    }).reset_index()

    # Rename columns for clarity
    customer_orders.columns = [
        'Customer ID', 'Total Orders', 'Total Sales',
        'Total Profit', 'First Purchase', 'Last Purchase'
    ]

    # Calculate customer tenure
    customer_orders['Customer Tenure Days'] = (
        customer_orders['Last Purchase'] - customer_orders['First Purchase']
    ).dt.days

    # Display first few rows
    print(customer_orders.head())