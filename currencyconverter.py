import streamlit as st
import requests
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Jishnu's Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CURRENCY DATA
# =========================================================

CURRENCIES = {
    "USD": ("🇺🇸", "US Dollar"),
    "EUR": ("🇪🇺", "Euro"),
    "GBP": ("🇬🇧", "British Pound"),
    "INR": ("🇮🇳", "Indian Rupee"),
    "JPY": ("🇯🇵", "Japanese Yen"),
    "AUD": ("🇦🇺", "Australian Dollar"),
    "CAD": ("🇨🇦", "Canadian Dollar"),
    "CHF": ("🇨🇭", "Swiss Franc"),
    "CNY": ("🇨🇳", "Chinese Yuan"),
    "SGD": ("🇸🇬", "Singapore Dollar"),
    "HKD": ("🇭🇰", "Hong Kong Dollar"),
    "NZD": ("🇳🇿", "New Zealand Dollar"),
    "SEK": ("🇸🇪", "Swedish Krona"),
    "NOK": ("🇳🇴", "Norwegian Krone"),
    "DKK": ("🇩🇰", "Danish Krone"),
    "PLN": ("🇵🇱", "Polish Zloty"),
    "CZK": ("🇨🇿", "Czech Koruna"),
    "HUF": ("🇭🇺", "Hungarian Forint"),
    "BRL": ("🇧🇷", "Brazilian Real"),
    "MXN": ("🇲🇽", "Mexican Peso"),
    "ZAR": ("🇿🇦", "South African Rand"),
    "THB": ("🇹🇭", "Thai Baht"),
    "TRY": ("🇹🇷", "Turkish Lira"),
    "ILS": ("🇮🇱", "Israeli New Shekel"),
    "KRW": ("🇰🇷", "South Korean Won")
}

CODES = list(CURRENCIES.keys())


# =========================================================
# SESSION STATE
# =========================================================

if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"

if "to_currency" not in st.session_state:
    st.session_state.to_currency = "INR"


# =========================================================
# CUSTOM CSS
# =========================================================

css = (
    "<style>"

    ".stApp{"
    "background:"
    "radial-gradient(circle at 10% 20%,rgba(0,229,255,.16),transparent 28%),"
    "radial-gradient(circle at 90% 10%,rgba(255,0,153,.16),transparent 28%),"
    "radial-gradient(circle at 50% 90%,rgba(123,31,162,.20),transparent 35%),"
    "linear-gradient(135deg,#09001f,#12002f,#001f3f);"
    "background-size:200% 200%;"
    "animation:bgMove 12s ease infinite;"
    "}"

    "@keyframes bgMove{"
    "0%{background-position:0% 50%;}"
    "50%{background-position:100% 50%;}"
    "100%{background-position:0% 50%;}"
    "}"

    "header{background:transparent!important;}"
    "#MainMenu{visibility:hidden;}"
    "footer{visibility:hidden;}"

    ".block-container{"
    "max-width:1080px;"
    "padding-top:28px;"
    "padding-bottom:40px;"
    "}"

    "h1{"
    "text-align:center!important;"
    "font-size:clamp(34px,5vw,58px)!important;"
    "font-weight:900!important;"
    "letter-spacing:-1px!important;"
    "background:linear-gradient(90deg,#9b5cff,#00e5ff,#ffffff,#ff00cc,#00e5ff);"
    "background-size:300% auto;"
    "-webkit-background-clip:text;"
    "-webkit-text-fill-color:transparent;"
    "animation:titleMove 5s linear infinite;"
    "}"

    "@keyframes titleMove{"
    "from{background-position:0% center;}"
    "to{background-position:300% center;}"
    "}"

    "h2{"
    "color:#ffffff!important;"
    "font-weight:800!important;"
    "}"

    "h3{"
    "color:#ffffff!important;"
    "font-weight:700!important;"
    "}"

    "p{"
    "color:#eeeeff!important;"
    "}"

    ".stMarkdown p{"
    "color:#eeeeff!important;"
    "}"

    ".stCaption,"
    "[data-testid='stCaptionContainer']{"
    "color:#cfd3ff!important;"
    "}"

    "label{"
    "color:#ffffff!important;"
    "font-weight:600!important;"
    "}"

    "[data-testid='stWidgetLabel'] label{"
    "color:#ffffff!important;"
    "}"

    "[data-testid='stWidgetLabel'] p{"
    "color:#ffffff!important;"
    "}"

    ".subtitle{"
    "text-align:center;"
    "color:#eeeeff!important;"
    "font-size:18px;"
    "margin-bottom:26px;"
    "}"

    "[data-testid='stVerticalBlockBorderWrapper']{"
    "border-radius:24px!important;"
    "border:1px solid rgba(255,255,255,.18)!important;"
    "background:rgba(255,255,255,.055)!important;"
    "box-shadow:0 18px 45px rgba(0,0,0,.28)!important;"
    "backdrop-filter:blur(15px);"
    "}"

    "div[data-baseweb='select']>div{"
    "min-height:50px!important;"
    "border-radius:14px!important;"
    "background:rgba(255,255,255,.96)!important;"
    "}"

    "div[data-baseweb='select'] span{"
    "color:#202035!important;"
    "}"

    "div[data-baseweb='select'] input{"
    "color:#202035!important;"
    "}"

    "div[data-testid='stNumberInput']>div{"
    "border-radius:14px!important;"
    "background:rgba(255,255,255,.96)!important;"
    "}"

    "div[data-testid='stNumberInput'] input{"
    "color:#202035!important;"
    "font-size:17px!important;"
    "font-weight:600!important;"
    "}"

    ".stButton>button{"
    "min-height:48px!important;"
    "border-radius:14px!important;"
    "font-weight:700!important;"
    "transition:transform .22s ease,box-shadow .22s ease!important;"
    "}"

    ".stButton>button:hover{"
    "transform:translateY(-3px)!important;"
    "box-shadow:0 10px 25px rgba(0,229,255,.20)!important;"
    "}"

    "button[kind='primary']{"
    "background:linear-gradient(90deg,#7b2cff,#00cfff,#ff00cc)!important;"
    "background-size:200% auto!important;"
    "color:#ffffff!important;"
    "border:none!important;"
    "animation:buttonMove 4s linear infinite;"
    "}"

    "@keyframes buttonMove{"
    "from{background-position:0% center;}"
    "to{background-position:200% center;}"
    "}"

    "[data-testid='stMetric']{"
    "background:rgba(255,255,255,.07);"
    "border:1px solid rgba(255,255,255,.14);"
    "border-radius:17px;"
    "padding:15px;"
    "transition:transform .2s ease;"
    "}"

    "[data-testid='stMetric'] label{"
    "color:#dfe3ff!important;"
    "}"

    "[data-testid='stMetricValue']{"
    "color:#ffffff!important;"
    "}"

    "[data-testid='stMetricDelta']{"
    "color:#ffffff!important;"
    "}"

    "[data-testid='stAlert']{"
    "color:#ffffff!important;"
    "}"

    ".currency-card{"
    "background:rgba(255,255,255,.07);"
    "border:1px solid rgba(255,255,255,.14);"
    "border-radius:18px;"
    "padding:14px 8px;"
    "text-align:center;"
    "min-height:110px;"
    "transition:transform .25s ease,box-shadow .25s ease;"
    "}"

    ".currency-card:hover{"
    "transform:translateY(-5px);"
    "box-shadow:0 12px 28px rgba(0,229,255,.13);"
    "}"

    "</style>"
)

st.markdown(
    css,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.title("💱 Jishnu's Currency Converter")

st.markdown(
    '<div class="subtitle">'
    '🌍 Convert currencies using the latest available global exchange rates'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# MAIN CONVERTER
# =========================================================

with st.container(border=True):

    st.subheader("💱 Currency Conversion")

    st.caption(
        "Select your currencies, enter an amount, and get the latest available exchange rate."
    )

    left, middle, right = st.columns(
        [1.35, 0.55, 1.35],
        gap="medium"
    )

    # -----------------------------------------------------
    # FROM CURRENCY
    # -----------------------------------------------------

    with left:

        from_currency = st.selectbox(
            "💰 From Currency",
            CODES,
            index=CODES.index(
                st.session_state.from_currency
            ),
            format_func=lambda x:
                f"{CURRENCIES[x][0]}  {x} — {CURRENCIES[x][1]}",
            key="from_select"
        )

    # -----------------------------------------------------
    # SWAP
    # -----------------------------------------------------

    with middle:

        st.write("")
        st.write("")

        swap = st.button(
            "🔄 Swap",
            use_container_width=True
        )

    # -----------------------------------------------------
    # TO CURRENCY
    # -----------------------------------------------------

    with right:

        to_currency = st.selectbox(
            "💵 To Currency",
            CODES,
            index=CODES.index(
                st.session_state.to_currency
            ),
            format_func=lambda x:
                f"{CURRENCIES[x][0]}  {x} — {CURRENCIES[x][1]}",
            key="to_select"
        )

    # -----------------------------------------------------
    # SWAP ACTION
    # -----------------------------------------------------

    if swap:

        st.session_state.from_currency = to_currency
        st.session_state.to_currency = from_currency

        st.rerun()

    st.write("")

    # -----------------------------------------------------
    # AMOUNT
    # -----------------------------------------------------

    amount = st.number_input(
        "💵 Enter Amount",
        min_value=0.01,
        value=100.00,
        step=1.00,
        format="%.2f"
    )

    st.write("")

    # -----------------------------------------------------
    # CONVERT BUTTON
    # -----------------------------------------------------

    convert = st.button(
        "✨ CONVERT NOW ✨",
        type="primary",
        use_container_width=True
    )


# =========================================================
# EXCHANGE RATE FUNCTION
# =========================================================

def get_rate(base_currency, target_currency):

    if base_currency == target_currency:

        return (
            1.0,
            datetime.now().strftime("%Y-%m-%d")
        )

    url = (
        "https://api.frankfurter.dev/v2/rate/"
        + base_currency.lower()
        + "/"
        + target_currency.lower()
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "rate" not in data:

        raise ValueError(
            "Exchange rate was not returned by the service."
        )

    rate = float(data["rate"])

    rate_date = data.get(
        "date",
        datetime.now().strftime("%Y-%m-%d")
    )

    return rate, rate_date


# =========================================================
# CONVERSION
# =========================================================

if convert:

    if amount <= 0:

        st.error(
            "⚠️ Please enter an amount greater than zero."
        )

    else:

        try:

            with st.spinner(
                "🌐 Fetching the latest exchange rate..."
            ):

                rate, rate_date = get_rate(
                    from_currency,
                    to_currency
                )

            result = amount * rate

            st.session_state.from_currency = from_currency
            st.session_state.to_currency = to_currency

            st.write("")

            # -------------------------------------------------
            # RESULT CARD
            # -------------------------------------------------

            with st.container(border=True):

                st.subheader("✨ Conversion Result")

                st.markdown(
                    f"## {CURRENCIES[to_currency][0]} "
                    f"{result:,.2f} {to_currency}"
                )

                st.caption(
                    f"{CURRENCIES[from_currency][0]} "
                    f"{amount:,.2f} {from_currency}"
                    f"  →  "
                    f"{CURRENCIES[to_currency][0]} "
                    f"{result:,.2f} {to_currency}"
                )

                st.write("")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "📈 Exchange Rate",
                        f"{rate:,.6f}"
                    )

                with col2:

                    st.metric(
                        "💰 Converted Amount",
                        f"{result:,.2f} {to_currency}"
                    )

                with col3:

                    st.metric(
                        "📅 Rate Date",
                        rate_date
                    )

                st.caption(
                    "🌐 Exchange-rate data provided by Frankfurter"
                )

            st.success(
                "✅ Conversion completed successfully!"
            )

            st.balloons()

        except requests.exceptions.RequestException:

            st.error(
                "❌ Could not connect to the exchange-rate service. "
                "Please check your internet connection and try again."
            )

        except (ValueError, KeyError):

            st.error(
                "❌ The exchange rate could not be retrieved "
                "for this currency pair."
            )

        except Exception as error:

            st.error(
                f"❌ Something went wrong: {error}"
            )


# =========================================================
# SUPPORTED CURRENCIES
# =========================================================

st.write("")
st.divider()

st.subheader("🌎 Supported Currencies")

st.caption(
    "Popular currencies available for conversion."
)

items = list(CURRENCIES.items())

for start in range(
    0,
    len(items),
    5
):

    columns = st.columns(
        5,
        gap="medium"
    )

    for column, item in zip(
        columns,
        items[start:start + 5]
    ):

        code, details = item

        flag, name = details

        with column:

            st.markdown(
                '<div class="currency-card">'
                f'<div style="font-size:28px">{flag}</div>'
                f'<div style="color:white;font-size:16px;font-weight:800">'
                f'{code}'
                f'</div>'
                f'<div style="color:#bfc0dc;font-size:11px">'
                f'{name}'
                f'</div>'
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💱 Jishnu's Currency Converter  •  "
    "🌍 Latest available exchange rates  •  "
    "Built with Python + Streamlit ❤️"
)
