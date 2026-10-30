import streamlit as st
import requests

# 1. Page Configuration and Styling Rules
st.set_page_config(
    page_title="Enterprise Churn Simulator", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Advanced CSS for a clean enterprise interface
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    
    .header-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    .card-box {
        padding: 24px;
        border-radius: 12px;
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 18px;
        border-bottom: 2px solid #F3F4F6;
        padding-bottom: 8px;
    }
    
    .metric-value {
        font-size: 54px;
        font-weight: 700;
        line-height: 1;
        margin: 15px 0;
    }
    
    /* Dynamic Color Classes */
    .risk-low { color: #10B981; }
    .risk-medium { color: #F59E0B; }
    .risk-high { color: #EF4444; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Header Banner
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight:700; font-size:32px;'>📊 Customer Churn Intelligence Hub</h1>
        <p style='margin:5px 0 0 0; opacity:0.9; font-size:15px;'>Decoupled Machine Learning Simulation Pipeline & 'What-If' Decision Studio</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Structural Grid Columns
col1, col2 = st.columns([4, 5], gap="large")

with col1:
    st.markdown('<div class="card-box"><div class="section-title">📋 Active Customer Profile</div>', unsafe_allow_html=True)
    
    contract = st.selectbox("Contract Terms Agreement", ["Month-to-month", "One year", "Two year"])
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    tech_support = st.radio("Enterprise Tech Support Subscribed?", ["Yes", "No"], horizontal=True)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    tenure = st.slider("Lifecycle Tenure Duration (Active Months)", 1, 72, 12)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    monthly_charges = st.slider("Calculated Monthly Billing Account Weight ($)", 15.0, 150.0, 65.0)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-box"><div class="section-title">🔮 Real-Time Model Inference</div>', unsafe_allow_html=True)
    
    payload = {
        "contract": contract,
        "tech_support": tech_support,
        "tenure": tenure,
        "monthly_charges": monthly_charges
    }
    
    try:
        # Querying local active Flask backend
        response = requests.post("http://localhost:5000/predict", json=payload)
        
        if response.status_code == 200:
            res = response.json()
            prob = res['churn_probability']
            risk = res['risk_level']
            
            # Map dynamic styles depending on severity
            color_class = "risk-high" if risk == "High" else "risk-medium" if risk == "Medium" else "risk-low"
            badge_label = " CRITICAL RISK ALERT" if risk == "High" else " MODERATE WARNING" if risk == "Low" else " SECURE CUSTOMER STATUS"
            
            # Custom styled visualization scorecard
            st.markdown(f"""
                <div style="background-color: #F9FAFB; padding: 20px; border-radius: 8px; text-align: center; border: 1px dashed #E5E7EB;">
                    <p style="margin: 0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; color: #6B7280; font-size: 13px;">Predicted Churn Probability</p>
                    <div class="metric-value {color_class}">{prob * 100:.1f}%</div>
                    <span style="font-weight: 700; font-size: 14px; color: #374151;">Current Classification Status: {risk}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            
            # Preserving actionable retention playbooks
            if risk == "High":
                st.error(" **Retention Directive:** This account has crossed standard volatility boundaries. Flag account and dispatch account management team to propose incentive lock-in configurations immediately.")
            elif risk == "Medium":
                st.warning(" **Preemptive Playbook:** Indicators point toward service friction. Schedule routine account wellness check-ins or look to cross-sell technical onboarding solutions.")
            else:
                st.success(" **Expansion Track:** Account is structurally sound. Identify avenues for premium service tiered expansion or upsell tracks during standard lifecycles.")
                
        else:
            st.error("Core operational API running but request vector parsing completely failed.")
            
    except requests.exceptions.ConnectionError:
        st.info(" **System Setup Required:** Please confirm your background Flask server engine (`backend.py`) is initialized and running live on port 5000.")
    
    st.markdown('</div>', unsafe_allow_html=True)
