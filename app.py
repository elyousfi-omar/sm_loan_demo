import streamlit as st
import pandas as pd
import uuid

st.set_page_config(
    page_title="Client Standing Checker",
    page_icon="🏅",
)

@st.cache_data
def load_summary_data():
    return pd.read_csv('data/user_summary.csv')

def load_transactions_data():
    return pd.read_csv('data/dummy_transactions.csv')

user_summary = load_summary_data()
all_transactions = load_transactions_data()

# st.logo("data/logo.png")
st.badge("New")

try:
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 350px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
    )
except:
    pass

with st.sidebar:
    with st.spinner("Loading..."):
        st.image("data/logo.png", width=200)
        st.title("AI Loan Assessment")
        st.markdown("This app helps you check your account standing and loan eligibility.")
        st.markdown("##")
        st.markdown("### Instructions")
        st.markdown("1. Enter your Primary Account Number.")
        st.markdown("2. Enter the desired loan amount.")
        st.markdown("3. Click on 'Check Standing' to see your account status.")
        st.markdown("##")
        st.chat_input(placeholder="Ask me about your account", accept_file=True)
        st.markdown("### Disclaimer")
        st.markdown("This is a demo application and does not represent real data.")
        st.markdown("Data is randomly generated using Faker https://github.com/joke2k/faker")
    

with st.form("Loan form"):
    account_number = st.text_input("Enter Primary Account Number", "")
    desirable_loan = st.number_input("Enter Desirable Loan Amount", min_value=0, step=1000, format="%d")
    st.form_submit_button("Check Standing")

special_id = uuid.uuid1()

if desirable_loan < 100:
    st.warning("We accept loans starting from $100. Please enter a valid amount.")
    st.stop()
elif desirable_loan > 50000:
    st.success("We accept automatic loans up to $50,000. Please enter a valid amount.")
    st.stop()

if account_number and desirable_loan > 0:
    
    user_row = user_summary[user_summary['primary_account_number'].astype(str) == account_number]
    if not user_row.empty:
        user_data = all_transactions[all_transactions['primary_account_number'].astype(str) == account_number]
        st.header(f"Welcome {user_data['cardholder_name'].values[0]}")
        st.divider()
        standing = user_row['standing'].values[0]
        if standing.upper() == 'LOW' and desirable_loan > 2000:
            st.warning(f"You won't be able to get a loan of ${desirable_loan}. For more details, please contact an agent.")
        elif standing.upper() == 'MEDIUM' and desirable_loan > 15000:
            st.warning(f"Sorry, it seems you won't be able to get a loan of ${desirable_loan}. For more details, please contact an agent.")
        elif standing.upper() == 'PLATINUM':
            st.success(f"🏅Congrats! You are able to get this loan amount, please contact an agent.")
        else:
            st.success(f"Congrats! You are able to get a ${desirable_loan} loan.")

        with st.expander("Show my transactions"):
            st.dataframe(user_data[["acquirer_reference_number", "transaction_type", "transaction_amount", "transaction_currency_code", "merchant_category_code", "card_acceptor_id", "merchant_name", "transaction_date"]].sort_values(by="transaction_date", ascending=False).reset_index(drop=True), use_container_width=True)
    else:
        st.error("Account number not found.")