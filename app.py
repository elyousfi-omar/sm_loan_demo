import streamlit as st
import pandas as pd
import uuid

st.set_page_config(
    page_title="Client Standing Checker",
    page_icon="🏅",
    layout="wide",
)

@st.cache_data
def load_summary_data():
    return pd.read_csv('data/user_summary.csv')

def load_transactions_data():
    return pd.read_csv('data/dummy_transactions.csv')

user_summary = load_summary_data()
all_transactions = load_transactions_data()

account_number = st.text_input("Enter Primary Account Number", "")
desirable_loan = st.number_input("Enter Desirable Loan Amount", min_value=0, step=1000, format="%d")

if account_number and desirable_loan > 0:
    special_id = uuid.uuid1()
    user_data = all_transactions[all_transactions['primary_account_number'].astype(str) == account_number]
    st.write(f"Welcome {user_data['cardholder_name'].values[0]}")
    user_row = user_summary[user_summary['primary_account_number'].astype(str) == account_number]
    if not user_row.empty:
        standing = user_row['predicted_standing'].values[0]
        if standing.upper() == 'LOW' and desirable_loan > 2000:
            st.warning(f"You won't be able to get a loan of ${desirable_loan}. For more details, please contact an agent with this id: {special_id}")
        elif standing.upper() == 'MEDIUM' and desirable_loan > 15000:
            st.warning(f"Sorry, it seems you won't be able to get a loan of ${desirable_loan}. For more details, please contact an agent with this id: {special_id}")
        elif standing.upper() == 'PLATINUM':
            st.success(f"🏅Congrats! You are able to get this loan amount, please contact an agent with this id: {special_id}")
        else:
            st.success(f"Congrats! You are able to get a ${desirable_loan} loan. For more information, please contact an agent with this id: {special_id}")

        st.success(f"Your Standing: **{standing.upper()}**")

        with st.expander("Show my transactions"):
            st.dataframe(user_data[["acquirer_reference_number", "transaction_type", "transaction_amount", "transaction_currency_code", "merchant_category_code", "card_acceptor_id", "merchant_name", "transaction_date"]].sort_values(by="transaction_date", ascending=False).reset_index(drop=True), use_container_width=True)
    else:
        st.error("Account number not found.")
