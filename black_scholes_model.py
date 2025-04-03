"""
Created on Sat Mar 29 16:04:29 2025

@author: joshuarogers
"""

import streamlit as st
from streamlit.runtime.scriptrunner import RerunException
import numpy as np
from scipy.stats import norm

N = norm.cdf


# Default Values for Each Param

DEFAULTS = {
    "S0": 100.0,
    "K": 100.0,
    "t": 1.0,
    "r": 0.05,
    "sigma": 0.2,
}


# Reset Overwrites Each Param

def reset_values():
    """Instead of deleting keys, just overwrite them with defaults."""
    for param, val in DEFAULTS.items():
        st.session_state[param] = val
    # Force an immediate update in the main script
    st.session_state["needs_rerun"] = True


# Callbacks: Update main param key

def update_from_slider(key):
    st.session_state[key] = st.session_state[key + "_slider"]
    st.session_state["needs_rerun"] = True

def update_from_input(key):
    st.session_state[key] = st.session_state[key + "_input"]
    st.session_state["needs_rerun"] = True


# Synced Slider + Number Input

def synced_slider_input(label, min_val, max_val, step, key):
    """One main key for each param, plus separate widget keys for slider & input."""
    # If the main key doesn't exist, set default from DEFAULTS
    if key not in st.session_state:
        st.session_state[key] = DEFAULTS[key]

    # Distinct widget keys
    slider_widget_key = key + "_slider"
    input_widget_key  = key + "_input"

    # Keep widget keys in sync with the main key
    st.session_state[slider_widget_key] = st.session_state[key]
    st.session_state[input_widget_key]  = st.session_state[key]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.slider(
            label,
            min_value=min_val,
            max_value=max_val,
            step=step,
            value=st.session_state[key],      # safe, we re-assign above
            key=slider_widget_key,
            on_change=update_from_slider,
            args=(key,)
        )
    with col2:
        st.number_input(
            "",
            min_value=min_val,
            max_value=max_val,
            step=step,
            value=st.session_state[key],
            key=input_widget_key,
            label_visibility="collapsed",
            on_change=update_from_input,
            args=(key,)
        )

    return st.session_state[key]


# Black-Scholes Functions

def BS_CALL(S0, K, t, r, sigma):
    d1 = (np.log(S0/K) + (r + sigma**2/2)*t) / (sigma*np.sqrt(t))
    d2 = d1 - sigma*np.sqrt(t)
    return S0 * N(d1) - K * np.exp(-r*t) * N(d2)

def BS_PUT(S0, K, t, r, sigma):
    d1 = (np.log(S0/K) + (r + sigma**2/2)*t) / (sigma*np.sqrt(t))
    d2 = d1 - sigma*np.sqrt(t)
    return K * np.exp(-r*t) * N(-d2) - S0 * N(-d1)


# Streamlit Setup

st.set_page_config(page_title="Black-Scholes Calculator", layout="centered")

st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h1 style='font-size: 3rem; color: #60A5FA; margin-bottom: 5px;'>Black-Scholes Option Calculator</h1>
        <p style='font-size: 1.2rem; color: #BBBBBB; margin-top: 0;'>A Project by Joshua Rogers</p>
    </div>
    """, unsafe_allow_html=True)

# Insert custom CSS for styling st.success() alerts:
st.markdown("""
<style>
/* Override st.success() default styling */
.stAlert {
    background-color: #1E3A8A !important; /* dark slate background, matching the overall page */
    border-left-color: #3B82F6 !important; /* bright blue accent to match the header */
    color: #E0F2FE !important; /* text color so it’s legible on dark slate */
}
</style>
""", unsafe_allow_html=True)


# Sidebar: Reset + Instant-Sync Inputs

with st.sidebar:
    st.header("Parameters")
    if st.button("Reset All to Defaults"):
        reset_values()

    # Create each param
    S0_val = synced_slider_input("Stock Price ($S_0$)",   50.0, 150.0, 0.1, "S0")
    K_val  = synced_slider_input("Strike Price (K)",      50.0, 150.0, 0.1, "K")
    t_val  = synced_slider_input("Time to Maturity (t)",  0.1,  2.0,   0.01,"t")
    r_val  = synced_slider_input("Risk-free Rate (r)",    0.0,  0.2,   0.001,"r")
    sigma_val = synced_slider_input("Volatility ($\\sigma$)", 0.05, 1.0, 0.01,"sigma")


# Final Results

st.markdown("---")
st.subheader("Option Prices")

call_price = BS_CALL(S0_val, K_val, t_val, r_val, sigma_val)
put_price  = BS_PUT(S0_val, K_val, t_val, r_val, sigma_val)
st.success(f"Call Option Price: `{call_price:.4f}`")
st.success(f"Put Option Price: `{put_price:.4f}`")

st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 0.8rem; color: #AAAAAA;'>
        © 2025 Joshua Rogers. Built with Streamlit.
    </div>
    """, unsafe_allow_html=True)


# End: Force Rerun if needed

if st.session_state.get("needs_rerun", False):
    st.session_state["needs_rerun"] = False
    raise RerunException("Instant update from callback or reset")












