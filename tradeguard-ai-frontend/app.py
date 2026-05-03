import requests
import streamlit as st
import pandas as pd
import plotly.express as px


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="TradeGuard AI",
    page_icon="📈",
    layout="wide"
)


def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None

    if "user" not in st.session_state:
        st.session_state.user = None


def get_auth_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def register_user(name, email, password):
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )
    return response


def login_user(email, password):
    # We are using 'data=' to force Form Data, and mapping email to 'username'
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password
    }
    
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        data=payload # MUST be 'data=', NOT 'json='
    )
    
    # 🚨 DEBUGGING: This will print the exact reason for the 422 in your terminal!
    if response.status_code == 422:
        print("\n" + "="*50)
        print("🚨 422 ERROR DETAIL FROM BACKEND:")
        print(response.text)
        print("="*50 + "\n")
        
    return response


def get_profile():
    response = requests.get(
        f"{API_BASE_URL}/auth/me",
        headers=get_auth_headers()
    )
    return response


def get_trades():
    response = requests.get(
        f"{API_BASE_URL}/trades/",
        headers=get_auth_headers()
    )
    return response


def get_summary():
    response = requests.get(
        f"{API_BASE_URL}/trades/analytics/summary",
        headers=get_auth_headers()
    )
    return response


def get_symbol_performance():
    response = requests.get(
        f"{API_BASE_URL}/trades/analytics/by-symbol",
        headers=get_auth_headers()
    )
    return response


def add_trade(data):
    response = requests.post(
        f"{API_BASE_URL}/trades/",
        json=data,
        headers=get_auth_headers()
    )
    return response


def upload_csv(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "text/csv"
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/trades/upload-csv",
        files=files,
        headers=get_auth_headers()
    )

    return response


def calculate_position_size(data):
    response = requests.post(
        f"{API_BASE_URL}/risk/position-size",
        json=data
    )
    return response

def predict_trade_risk(data):
    response = requests.post(
        f"{API_BASE_URL}/ml/predict-risk",
        json=data,
        headers=get_auth_headers()
    )
    return response

def show_ml_prediction_page():
    st.title("🤖 ML Trade Risk Prediction")

    st.write(
        """
        This tool does not predict future market direction.
        It predicts whether your trade setup looks Low Risk, Medium Risk, or High Risk.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        symbol = st.selectbox(
            "Symbol",
            ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSDT", "USDJPY"]
        )

        trade_type = st.selectbox(
            "Trade Type",
            ["buy", "sell"]
        )

        session = st.selectbox(
            "Trading Session",
            ["Asian", "London", "New York"]
        )

        risk_reward = st.number_input(
            "Risk-Reward Ratio",
            min_value=0.1,
            value=1.5,
            format="%.2f"
        )

    with col2:
        stop_loss_pips = st.number_input(
            "Stop Loss Pips",
            min_value=1.0,
            value=30.0,
            format="%.2f"
        )

        lot_size = st.number_input(
            "Lot Size",
            min_value=0.01,
            value=0.10,
            format="%.2f"
        )

        recent_loss_streak = st.number_input(
            "Recent Loss Streak",
            min_value=0,
            value=0,
            step=1
        )

    if st.button("Predict Trade Risk"):
        data = {
            "symbol": symbol,
            "trade_type": trade_type,
            "session": session,
            "risk_reward": risk_reward,
            "stop_loss_pips": stop_loss_pips,
            "lot_size": lot_size,
            "recent_loss_streak": recent_loss_streak
        }

        response = predict_trade_risk(data)

        if response.status_code == 200:
            result = response.json()

            risk_label = result["risk_label"]

            if risk_label == "Low Risk":
                st.success(f"Prediction: {risk_label}")

            elif risk_label == "Medium Risk":
                st.warning(f"Prediction: {risk_label}")

            else:
                st.error(f"Prediction: {risk_label}")

            st.metric("Model Confidence", f"{result['confidence']}%")
            st.info(result["explanation"])

        else:
            st.error(response.json().get("detail", "Prediction failed."))
            
def show_landing_page():
    st.title("📈 TradeGuard AI")
    st.subheader("Smart Trading Journal & Risk Management SaaS")

    st.write(
        """
        TradeGuard AI helps forex and crypto traders track their trades,
        analyze performance, manage risk, and improve trading discipline.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Trade Analytics")

    with col2:
        st.success("🛡️ Risk Management")

    with col3:
        st.warning("🤖 AI-Style Feedback")

    st.markdown("---")
    st.write("Please login or create an account from the sidebar.")


def show_auth_page():
    st.sidebar.title("Account")

    auth_choice = st.sidebar.radio(
        "Choose option",
        ["Login", "Register"]
    )

    if auth_choice == "Register":
        st.sidebar.subheader("Create Account")

        name = st.sidebar.text_input("Name")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Register"):
            if not name or not email or not password:
                st.sidebar.error("Please fill all fields.")
            else:
                response = register_user(name, email, password)

                if response.status_code == 200:
                    st.sidebar.success("Account created. Now login.")
                else:
                    st.sidebar.error(response.json().get("detail", "Registration failed."))

    else:
        st.sidebar.subheader("Login")

        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if not email or not password:
                st.sidebar.error("Please enter email and password.")
            else:
                response = login_user(email, password)

                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]

                    profile_response = get_profile()

                    if profile_response.status_code == 200:
                        st.session_state.user = profile_response.json()

                    st.sidebar.success("Login successful.")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid email or password.")


def show_sidebar_after_login():
    st.sidebar.success(f"Logged in as {st.session_state.user['name']}")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()


def show_dashboard():
    st.title("📊 Dashboard")

    summary_response = get_summary()

    if summary_response.status_code != 200:
        st.error("Could not load dashboard data.")
        return

    summary = summary_response.json()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Trades", summary["total_trades"])

    with col2:
        st.metric("Net Profit/Loss", summary["total_profit_loss"])

    with col3:
        st.metric("Win Rate", f"{summary['win_rate']}%")

    with col4:
        st.metric("Risk Score", summary["risk_score"])

    col5, col6 = st.columns(2)

    with col5:
        st.metric("Average Profit", summary["average_profit"])

    with col6:
        st.metric("Average Loss", summary["average_loss"])

    st.subheader("🤖 AI Feedback")
    st.info(summary["ai_feedback"])

    st.markdown("---")

    trades_response = get_trades()

    if trades_response.status_code == 200:
        trades = trades_response.json()

        if trades:
            df = pd.DataFrame(trades)

            st.subheader("Profit/Loss Chart")

            fig = px.line(
                df,
                x="trade_date",
                y="profit_loss",
                markers=True,
                title="Trade-by-Trade Profit/Loss"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Recent Trades")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No trades found. Add trades or upload CSV first.")


def show_add_trade_page():
    st.title("➕ Add Trade")

    with st.form("add_trade_form"):
        col1, col2 = st.columns(2)

        with col1:
            symbol = st.text_input("Symbol", placeholder="EURUSD")
            trade_type = st.selectbox("Trade Type", ["buy", "sell"])
            entry_price = st.number_input("Entry Price", min_value=0.0, format="%.5f")
            exit_price = st.number_input("Exit Price", min_value=0.0, format="%.5f")
            lot_size = st.number_input("Lot Size", min_value=0.0, format="%.2f")

        with col2:
            stop_loss = st.number_input("Stop Loss", min_value=0.0, format="%.5f")
            take_profit = st.number_input("Take Profit", min_value=0.0, format="%.5f")
            profit_loss = st.number_input("Profit/Loss", format="%.2f")
            risk_reward = st.number_input("Risk Reward", min_value=0.0, format="%.2f")
            emotion = st.text_input("Emotion", placeholder="calm, angry, confident")

        mistake = st.text_area("Mistake", placeholder="Example: revenge trade, early entry")
        lesson = st.text_area("Lesson", placeholder="Example: wait for confirmation")

        submitted = st.form_submit_button("Save Trade")

        if submitted:
            trade_data = {
                "symbol": symbol,
                "trade_type": trade_type,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "lot_size": lot_size,
                "stop_loss": stop_loss if stop_loss > 0 else None,
                "take_profit": take_profit if take_profit > 0 else None,
                "profit_loss": profit_loss,
                "risk_reward": risk_reward if risk_reward > 0 else None,
                "emotion": emotion,
                "mistake": mistake,
                "lesson": lesson
            }

            response = add_trade(trade_data)

            if response.status_code == 200:
                st.success("Trade saved successfully.")
            else:
                st.error(response.json().get("detail", "Failed to save trade."))


def show_upload_csv_page():
    st.title("📁 Upload Trade CSV")

    st.write("Your CSV should contain these required columns:")

    st.code(
        "symbol, trade_type, entry_price, exit_price, lot_size, profit_loss"
    )

    uploaded_file = st.file_uploader(
        "Upload your trade history CSV",
        type=["csv"]
    )

    if uploaded_file is not None:
        st.write("Preview:")

        preview_df = pd.read_csv(uploaded_file)
        st.dataframe(preview_df.head(), use_container_width=True)

        uploaded_file.seek(0)

        if st.button("Upload to Database"):
            response = upload_csv(uploaded_file)

            if response.status_code == 200:
                st.success(response.json()["message"])
                st.write(f"Inserted trades: {response.json()['inserted_trades']}")
            else:
                st.error(response.json().get("detail", "CSV upload failed."))


def show_analytics_page():
    st.title("📈 Analytics")

    symbol_response = get_symbol_performance()

    if symbol_response.status_code != 200:
        st.error("Could not load analytics.")
        return

    symbol_data = symbol_response.json()

    if not symbol_data:
        st.warning("No analytics available yet.")
        return

    df = pd.DataFrame(symbol_data).T
    df = df.reset_index().rename(columns={"index": "symbol"})

    st.subheader("Symbol-Wise Performance")
    st.dataframe(df, use_container_width=True)

    fig = px.bar(
        df,
        x="symbol",
        y="total_profit_loss",
        title="Profit/Loss by Symbol"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        df,
        x="symbol",
        y="total_trades",
        title="Number of Trades by Symbol"
    )

    st.plotly_chart(fig2, use_container_width=True)


def show_risk_calculator_page():
    st.title("🛡️ Risk Calculator")

    col1, col2 = st.columns(2)

    with col1:
        account_balance = st.number_input("Account Balance", min_value=0.0, value=1000.0)
        risk_percent = st.number_input("Risk Percent", min_value=0.1, value=1.0)
        stop_loss_pips = st.number_input("Stop Loss Pips", min_value=1.0, value=30.0)
        pip_value = st.number_input("Pip Value", min_value=0.1, value=10.0)

    if st.button("Calculate Position Size"):
        data = {
            "account_balance": account_balance,
            "risk_percent": risk_percent,
            "stop_loss_pips": stop_loss_pips,
            "pip_value": pip_value
        }

        response = calculate_position_size(data)

        if response.status_code == 200:
            result = response.json()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Risk Amount", result["risk_amount"])

            with col2:
                st.metric("Recommended Lot Size", result["recommended_lot_size"])

            st.warning(result["warning"])
        else:
            st.error("Calculation failed.")


def main():
    init_session()

    show_auth_page()

    if st.session_state.token is None:
        show_landing_page()
        return

    show_sidebar_after_login()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Trade",
            "Upload CSV",
            "Analytics",
            "Risk Calculator",
            "ML Prediction"
        ]
    )

    if page == "Dashboard":
        show_dashboard()

    elif page == "Add Trade":
        show_add_trade_page()

    elif page == "Upload CSV":
        show_upload_csv_page()

    elif page == "Analytics":
        show_analytics_page()

    elif page == "Risk Calculator":
        show_risk_calculator_page()
    
    elif page == "ML Prediction":
        show_ml_prediction_page()

if __name__ == "__main__":
    main()
