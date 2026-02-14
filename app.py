import random
import time
from datetime import datetime

import streamlit as st

# =========================
# EDIT THESE TWO VALUES ✅
# =========================
PROPOSE_DATE = "2024-11-03"   # YYYY-MM-DD  (change this)
PROPOSE_DAY  = "Sunday"       # Monday/Tuesday/... (change this)

GF_NAME   = "Dipika"
YOUR_NAME = "Tanmay"

st.set_page_config(page_title="PookieBear 💘", page_icon="🧸", layout="centered")

# -------------------------
# Helpers
# -------------------------
def norm(s: str) -> str:
    return "".join(ch.lower() for ch in s.strip() if ch.isalnum())

def parse_date_guess(s: str):
    """
    Very forgiving date parsing without extra libraries.
    Accepts:
    - YYYY-MM-DD
    - DD/MM/YYYY or DD-MM-YYYY
    - '3 Nov 2024' / '03 November 2024'
    """
    s = s.strip()
    # Try ISO first
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%d %B %Y", "%d %b, %Y", "%d %B, %Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None

def correct_proposal_answer(date_text: str, day_text: str) -> bool:
    d = parse_date_guess(date_text)
    if d is None:
        return False
    expected = datetime.strptime(PROPOSE_DATE, "%Y-%m-%d").date()
    return (d == expected) and (norm(day_text) == norm(PROPOSE_DAY))

# -------------------------
# Session state
# -------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "boot"
if "no_tries" not in st.session_state:
    st.session_state.no_tries = 0
if "no_mode" not in st.session_state:
    st.session_state.no_mode = "left"  # left/right/vanish
if "spark" not in st.session_state:
    st.session_state.spark = random.randint(1, 999999)

# -------------------------
# Gorgeous PookieBear theme CSS
# -------------------------
st.markdown(
    f"""
<style>
/* Background */
.stApp {{
  background: radial-gradient(circle at 10% 10%, rgba(255,182,193,0.35), transparent 40%),
              radial-gradient(circle at 90% 30%, rgba(255,105,180,0.25), transparent 45%),
              radial-gradient(circle at 50% 90%, rgba(173,216,230,0.18), transparent 50%),
              linear-gradient(160deg, #0b0b10 0%, #0f0f18 35%, #0b0b10 100%);
}}

/* Card */
.pookie-card {{
  padding: 18px 18px 14px 18px;
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,0.14);
  backgro
