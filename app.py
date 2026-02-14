import random
import time
import streamlit as st

GF_NAME   = "Dipika"
YOUR_NAME = "Tanmay"

st.set_page_config(page_title="PookieBear 💘", page_icon="🧸", layout="centered")

# -------------------------
# Session state
# -------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "boot"
if "no_tries" not in st.session_state:
    st.session_state.no_tries = 0

# -------------------------
# Cute CSS
# -------------------------
st.markdown(
"""
<style>
.stApp {
  background: radial-gradient(circle at 20% 20%, rgba(255,182,193,0.35), transparent 40%),
              radial-gradient(circle at 80% 30%, rgba(255,105,180,0.25), transparent 45%),
              linear-gradient(160deg, #0b0b10 0%, #0f0f18 50%, #0b0b10 100%);
}

/* floating hearts */
@keyframes floatUp {
  0% {transform: translateY(10px); opacity:0}
  20%{opacity:1}
  100%{transform: translateY(-600px); opacity:0}
}
.heart {
 position:fixed;
 bottom:-30px;
 font-size:22px;
 animation: floatUp linear infinite;
}
.h1{left:10%;animation-duration:7s}
.h2{left:25%;animation-duration:9s}
.h3{left:40%;animation-duration:6s}
.h4{left:55%;animation-duration:10s}
.h5{left:70%;animation-duration:8s}
.h6{left:85%;animation-duration:11s}

/* card */
.card{
padding:20px;
border-radius:22px;
background:rgba(255,255,255,0.06);
border:1px solid rgba(255,255,255,0.15);
backdrop-filter:blur(10px);
text-align:center;
}

/* title */
.title{font-size:46px;font-weight:900}
.subtitle{font-size:18px;opacity:.85}

/* buttons */
div.stButton>button{
height:60px;
font-size:20px;
border-radius:18px;
font-weight:800;
background:rgba(255,255,255,0.08);
}
</style>

<div class="heart h1">💖</div>
<div class="heart h2">💘</div>
<div class="heart h3">💞</div>
<div class="heart h4">💗</div>
<div class="heart h5">🫶</div>
<div class="heart h6">💓</div>
""",
unsafe_allow_html=True)

# -------------------------
# Boot screen
# -------------------------
def boot():
    st.markdown(f"""
    <div class="card">
    <div class="title">PookieBearOS 🧸💘</div>
    <div class="subtitle">Booting cuddles for {GF_NAME}...</div>
    </div>
    """, unsafe_allow_html=True)

    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.015)
        bar.progress(i+1)

    if st.button("Enter 💞"):
        st.session_state.stage = "question"
        st.rerun()

# -------------------------
# Question screen
# -------------------------
def question():
    st.markdown(f"""
    <div class="card">
    <div class="title">{GF_NAME} 💌</div>
    <div class="subtitle">Will you be my Valentine?</div>
    </div>
    """, unsafe_allow_html=True)

    mode = random.choice(["left","right","hide"])

    if mode=="left":
        col_no,col_yes=st.columns(2)
    else:
        col_yes,col_no=st.columns(2)

    with col_yes:
        if st.button("YES 💞"):
            st.session_state.stage="yes"
            st.rerun()

    with col_no:
        if mode=="hide":
            st.write("NO button is shy 🙈")
        else:
            if st.button("NO 🙃"):
                st.session_state.no_tries+=1
                st.warning(random.choice([
                    "NO ran away 🏃‍♀️",
                    "That option doesn't exist ❌",
                    "pookiebear says try again 🧸",
                    "system error: no not found 💘"
                ]))
                st.rerun()

# -------------------------
# Yes screen
# -------------------------
def yes_screen():
    st.balloons()
    st.markdown(f"""
    <div class="card">
    <div class="title">YAYYYYY 🎉</div>
    <div class="subtitle">{GF_NAME}, you just made {YOUR_NAME} the happiest person ❤️</div>
    <p>Feb 14 is now ours 💘</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Router
# -------------------------
if st.session_state.stage=="boot":
    boot()
elif st.session_state.stage=="question":
    question()
else:
    yes_screen()
