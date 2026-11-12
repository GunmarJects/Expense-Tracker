import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💸 My Expense Tracker")
st.write("Track your spending and see where your money goes.")

# --- NEW: Currency Selector ---
currency = st.selectbox("Select your currency:", ["R (ZAR)", "$ (USD)", "€ (EUR)", "£ (GBP)", "¥ (JPY)"])
currency_symbol = currency.split(" ")[0] # This splits "R (ZAR)" and grabs just the "R"

# 1. We use 'session_state' so the app remembers the data when it refreshes
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# 2. The input form
with st.form("expense_form"):
    st.subheader("Add a new expense")
    item = st.text_input("What did you buy? (e.g., Bread, Data, Uber)")
    amount = st.number_input(f"How much did it cost? ({currency_symbol})", min_value=1.0, step=10.0)
    
    submitted = st.form_submit_button("Add Expense")
    
    if submitted and item:
        # Add to our list
        st.session_state.expenses.append({"Item": item, "Amount": amount})
        st.success(f"Added {item} for {currency_symbol}{amount}!")

# 3. Display the data if there are expenses
if st.session_state.expenses:
    st.divider()
    st.subheader("Your Expenses")
    
    # Convert the list to a Pandas DataFrame
    df = pd.DataFrame(st.session_state.expenses)
    
    # Show the table
    st.dataframe(df, use_container_width=True)
    
    # Show the total with the selected currency
    total = df["Amount"].sum()
    st.metric(label="Total Spent", value=f"{currency_symbol} {total:.2f}")
    
    # 4. Draw the Pie Chart
    st.subheader("Spending Breakdown")
    
    category_totals = df.groupby("Item")["Amount"].sum()
    
    fig, ax = plt.subplots()
    # We add the currency symbol to the pie chart labels
    labels = [f"{currency_symbol}{val:.2f}" for val in category_totals]
    ax.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    
    st.pyplot(fig)
    
    # 5. A button to clear everything
    if st.button("Clear All Expenses"):
        st.session_state.expenses = []
        st.rerun()
else:
    st.info("No expenses added yet. Add one above!")