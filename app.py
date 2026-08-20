"""
Fraud SMS Classifier - Compact Single-Page Version
Author: Isa Haruna Aliyu
3MTT NextGen AI/ML Capstone Project
"""

import streamlit as st
import joblib
import re
import os

st.set_page_config(
    page_title="Fraud SMS Classifier",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MODEL_PATH = os.path.join("models", "fraud_sms_model.pkl")
VECTORIZER_PATH = os.path.join("models", "tfidf_vectorizer.pkl")

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

try:
    model, vectorizer = load_artifacts()
    ARTIFACTS_LOADED = True
except Exception as e:
    ARTIFACTS_LOADED = False
    LOAD_ERROR = str(e)

NIGERIAN_FRAUD_KEYWORDS = {
    "bvn": "BVN", "nin": "NIN", "kyc": "KYC", "otp": "OTP", "pos": "POS",
    "atm": "ATM", "verify": "Verify", "block": "Block", "blocked": "Blocked",
    "click": "Click", "link": "Link", "won": "Won", "winner": "Winner",
    "claim": "Claim", "prize": "Prize", "urgent": "Urgent", "free": "Free",
    "credited": "Credited", "debited": "Debited", "reactivate": "Reactivate",
    "suspend": "Suspend", "suspended": "Suspended", "account": "Account",
    "call": "Call", "sms": "SMS", "txt": "Txt", "cash": "Cash", "grant": "Grant",
    "reward": "Reward", "investment": "Investment", "double": "Double",
    "processing fee": "Fee", "clearance": "Clearance", "recruitment": "Recruitment",
    "selected": "Selected", "congratulations": "Congratulations", "expire": "Expire",
    "limited": "Limited", "immediately": "Immediately", "confirm": "Confirm"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return ' '.join(text.split())

def get_suspicious_keywords(original_text):
    text_lower = original_text.lower()
    return [kw for kw in NIGERIAN_FRAUD_KEYWORDS.keys() if kw in text_lower]

def classify_risk_level(score_pct):
    if score_pct < 40:
        return "Low", "#28a745"
    elif score_pct < 65:
        return "Medium", "#ffc107"
    else:
        return "High", "#dc3545"

st.markdown("""
    <style>
    * { margin: 0; padding: 0; }
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0f1419 0%, #1a2a3a 100%); }
    .header { background: linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 100%); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #00d4ff; }
    .header h1 { font-size: 1.6rem; color: #00d4ff; font-weight: 800; margin: 0; }
    .header p { color: #a0b0c0; font-size: 0.8rem; margin: 4px 0 0 0; }
    .section-title { color: #fff; font-size: 0.95rem; font-weight: 700; margin: 12px 0 6px 0; border-bottom: 1px solid #00d4ff; padding-bottom: 4px; }
    .result-fraud { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border: 2px solid #dc3545; color: #721c24; padding: 10px; border-radius: 8px; text-align: center; font-weight: 700; margin: 8px 0; font-size: 1.1rem; }
    .result-safe { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: 2px solid #28a745; color: #155724; padding: 10px; border-radius: 8px; text-align: center; font-weight: 700; margin: 8px 0; font-size: 1.1rem; }
    .risk-score { background: rgba(0, 212, 255, 0.05); border-left: 3px solid #00d4ff; padding: 8px; margin: 8px 0; border-radius: 6px; font-size: 0.85rem; color: #b0c4de; }
    .keyword-badge { display: inline-block; background: #fff3cd; color: #856404; border: 1px solid #ffc107; border-radius: 15px; padding: 3px 8px; margin: 3px 3px 3px 0; font-size: 0.75rem; font-weight: 600; }
    .safety { background: rgba(255, 193, 7, 0.1); border-left: 3px solid #ffc107; padding: 8px; margin: 8px 0; border-radius: 6px; font-size: 0.8rem; color: #f0e68c; line-height: 1.4; }
    .footer { text-align: center; color: #555; font-size: 0.65rem; margin-top: 10px; padding-top: 8px; border-top: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>FRAUD SMS CLASSIFIER</h1><p>Detect fraudulent SMS targeting Nigerians</p></div>', unsafe_allow_html=True)

if not ARTIFACTS_LOADED:
    st.error(f"Error: {LOAD_ERROR}")
    st.stop()

st.markdown('<div class="section-title">Quick Examples</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("BVN Scam", use_container_width=True, key="btn1"):
        st.session_state.msg = "Dear Customer your ATM card blocked BVN update click http://verify-bvn.com reactivate urgent"
with col2:
    if st.button("Lottery Scam", use_container_width=True, key="btn2"):
        st.session_state.msg = "CONGRATULATIONS won N2500000 MTN Promo call 08011122233 immediately claim prize"
with col3:
    if st.button("Safe Alert", use_container_width=True, key="btn3"):
        st.session_state.msg = "GTBank account credited N25000 JOHN DOE balance N87340"

if "msg" not in st.session_state:
    st.session_state.msg = ""

st.markdown('<div class="section-title">SMS Input</div>', unsafe_allow_html=True)
msg = st.text_area("", value=st.session_state.msg, placeholder="Paste SMS...", height=50, label_visibility="collapsed")

col1, col2 = st.columns([2, 1])
with col1:
    scan = st.button("Scan", use_container_width=True, type="primary")
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.msg = ""
        st.rerun()

if scan and msg and msg.strip():
    cleaned = clean_text(msg)
    if cleaned:
        vec = vectorizer.transform([cleaned])
        pred = model.predict(vec)[0]
        score = model.decision_function(vec)[0]
        risk_pct = round((1 / (1 + pow(2.718281828, -score))) * 100, 1)
        keywords = get_suspicious_keywords(msg)
        risk_level, risk_color = classify_risk_level(risk_pct)
        
        st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
        
        if pred == 1:
            st.markdown('<div class="result-fraud">FRAUD DETECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-safe">SAFE / LEGITIMATE</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="risk-score">Risk Score: {risk_pct}% | Level: <span style="color:{risk_color}; font-weight:700;">{risk_level}</span></div>', unsafe_allow_html=True)
        
        if keywords:
            badges = "".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords])
            st.markdown(f'<div class="section-title">Indicators</div>{badges}', unsafe_allow_html=True)
        
        advice = "Do NOT click links or share passwords. Verify via official channel." if pred == 1 else "Message appears safe. Verify requests independently."
        st.markdown(f'<div class="safety">{advice}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Built by Isa Haruna Aliyu | 3MTT NextGen AI/ML Capstone Project |Powered by Linear SVM + TF-IDF</div>', unsafe_allow_html=True)