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
  background: rgba(255,255,255,0.06);
  box-shadow: 0 14px 55px rgba(0,0,0,0.35);
  backdrop-filter: blur(8px);
}}

/* Title */
.pookie-title {{
  font-size: 46px;
  font-weight: 900;
  letter-spacing: -0.5px;
  margin: 0;
}}
.pookie-sub {{
  font-size: 18px;
  opacity: 0.86;
  margin-top: 6px;
}}

/* Animated floating hearts */
@keyframes floatUp {{
  0%   {{ transform: translateY(10px) scale(0.9); opacity: 0; }}
  15%  {{ opacity: 0.95; }}
  100% {{ transform: translateY(-520px) scale(1.2); opacity: 0; }}
}}
.heart {{
  position: fixed;
  bottom: -40px;
  font-size: 20px;
  animation: floatUp linear infinite;
  filter: drop-shadow(0 4px 12px rgba(255,105,180,0.45));
  z-index: 0;
}}
/* place hearts */
{''.join([f'.h{i}{{left:{random.randint(3,97)}%; animation-duration:{random.randint(6,12)}s; animation-delay:{random.randint(0,7)}s;}}' for i in range(1,18)])}

/* PookieBear wiggle */
@keyframes wiggle {{
  0% {{ transform: rotate(0deg) scale(1); }}
  25% {{ transform: rotate(-2deg) scale(1.02); }}
  50% {{ transform: rotate(2deg) scale(1.04); }}
  75% {{ transform: rotate(-2deg) scale(1.02); }}
  100% {{ transform: rotate(0deg) scale(1); }}
}}
.pookiebear {{
  display: inline-block;
  animation: wiggle 2.2s ease-in-out infinite;
  transform-origin: 50% 90%;
}}

/* Buttons */
div.stButton > button {{
  border-radius: 18px !important;
  height: 58px !important;
  font-size: 18px !important;
  font-weight: 800 !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  background: rgba(255,255,255,0.08) !important;
}}
div.stButton > button:hover {{
  background: rgba(255,255,255,0.14) !important;
  transform: translateY(-1px);
}}
.smallnote {{
  font-size: 13px; opacity: 0.78;
}}
.pill {{
  display:inline-block; padding:6px 10px; border-radius:999px;
  border:1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.06);
  font-size: 13px; opacity: 0.9;
}}
.center {{ text-align:center; }}
</style>

<!-- hearts -->
<div class="heart h1">💖</div><div class="heart h2">💘</div><div class="heart h3">💞</div><div class="heart h4">💗</div>
<div class="heart h5">🫶</div><div class="heart h6">💓</div><div class="heart h7">💖</div><div class="heart h8">💘</div>
<div class="heart h9">💞</div><div class="heart h10">💗</div><div class="heart h11">🫶</div><div class="heart h12">💓</div>
<div class="heart h13">💖</div><div class="heart h14">💘</div><div class="heart h15">💞</div><div class="heart h16">💗</div>
<div class="heart h17">🫶</div>
""",
    unsafe_allow_html=True
)

# -------------------------
# Screens
# -------------------------
def boot():
    st.markdown(
        f"""
<div class="pookie-card center">
  <p class="pookie-title">PookieBearOS <span class="pookiebear">🧸</span>💘</p>
  <p class="pookie-sub">Booting cuddles, kisses, and chaos… for <b>{GF_NAME}</b></p>
  <span class="pill">Status: dangerously in love</span>
</div>
""",
        unsafe_allow_html=True
    )

    bar = st.progress(0)
    labels = [
        "Loading pookiebear.dll",
        "Warming up heart.exe",
        "Calibrating butterflies 🦋",
        "Initializing 'ask the question' module"
    ]
    p = 0
    for lab in labels:
        st.caption(lab)
        for _ in range(25):
            p += 1
            bar.progress(min(100, int(p / (len(labels)*25) * 100)))
            time.sleep(0.02)
    st.success("Boot complete ✅")

    st.markdown("<div class='center'>✨ 🧸 💖 💘 💞 ✨</div>", unsafe_allow_html=True)
    if st.button("Continue ➜"):
        st.session_state.stage = "verify"
        st.rerun()

def verify():
    st.markdown(
        f"""
<div class="pookie-card">
  <p class="pookie-title">Proof you’re my pookie 🧸</p>
  <p class="pookie-sub">{GF_NAME}, type the <b>date</b> and the <b>day</b> I proposed to you 😌</p>
  <div class="smallnote">Examples: 2024-11-03 / 03-11-2024 / 3 Nov 2024</div>
</div>
""",
        unsafe_allow_html=True
    )

    date_text = st.text_input("📅 The date", placeholder="e.g., 2024-11-03")
    day_text  = st.text_input("🗓️ The day",  placeholder="e.g., Sunday")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Verify ✅"):
            if correct_proposal_answer(date_text, day_text):
                st.success("Correct 😭💖 okay pookiebear access granted!")
                st.session_state.stage = "question"
                st.rerun()
            else:
                st.error("Nope 😌 try again (you got this).")
    with c2:
        if st.button("Hint 🫣"):
            st.info("It’s the day you made me your boyfriend. Think back to that moment 🧸💞")

def question():
    st.markdown(
        f"""
<div class="pookie-card center">
  <p class="pookie-title">{GF_NAME}… 💌</p>
  <p class="pookie-sub">One question. The cutest question. The pookiest question.</p>
  <div class="center">🧸💖🧸💖🧸</div>
</div>
""",
        unsafe_allow_html=True
    )
    st.markdown("<h2 class='center'>Will you be my Valentine?</h2>", unsafe_allow_html=True)

    # Make the NO button misbehave
    st.session_state.no_mode = random.choice(["left", "right", "vanish", "left", "right"])

    left_first = (st.session_state.no_mode == "left")
    vanish = (st.session_state.no_mode == "vanish")

    if left_first:
        col_no, col_yes = st.columns(2, gap="large")
    else:
        col_yes, col_no = st.columns(2, gap="large")

    with col_yes:
        if st.button("YES 💞"):
            st.session_state.stage = "yes"
            st.rerun()

    with col_no:
        if vanish:
            st.markdown("<div class='smallnote center'>NO is… um… shy today 🙈</div>", unsafe_allow_html=True)
            if st.button("NO 🙃 (catch me!)"):
                # if she clicks it, make it “poof”
                st.session_state.no_tries += 1
                st.toast("💨 NO vanished into the void", icon="💨")
                st.rerun()
        else:
            if st.button("NO 🙃"):
                st.session_state.no_tries += 1
                st.rerun()

    # Reactions to NO
    if st.session_state.no_tries > 0:
        msgs = [
            "❌ NO button is decorative.",
            "👀 that was… not the vibe.",
            "🧸 pookiebear says: try again.",
            "💘 timeline error: 'no' not found.",
            "🏃‍♀️ NO ran away. It’s scared of love.",
        ]
        st.warning(msgs[min(st.session_state.no_tries - 1, len(msgs) - 1)])

        if st.session_state.no_tries >= 4:
            st.info("Okay okay… I’ll ask nicely: please press YES 😭💖")

def yes_screen():
    st.balloons()
    st.markdown(
        f"""
<div class="pookie-card center">
  <p class="pookie-title">YAYYYYY 🎉🧸💖</p>
  <p class="pookie-sub"><b>{GF_NAME}</b>, you just made <b>{YOUR_NAME}</b> the happiest person ❤️</p>
  <p>📅 Valentine date scheduled: <b>Feb 14</b> (all day)</p>
  <p>🍫 Add-ons: chocolate, flowers, forehead kisses, unlimited attention</p>
  <p class="smallnote">PS: screenshot this and send it to me 😌</p>
</div>
""",
        unsafe_allow_html=True
    )

    if st.button("Replay 🔁"):
        st.session_state.stage = "boot"
        st.session_state.no_tries = 0
        st.session_state.spark = random.randint(1, 999999)
        st.rerun()

# -------------------------
# Router
# -------------------------
if st.session_state.stage == "boot":
    boot()
elif st.session_state.stage == "verify":
    verify()
elif st.session_state.stage == "question":
    question()
elif st.session_state.stage == "yes":
    yes_screen()
