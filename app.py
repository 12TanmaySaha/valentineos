import time
import streamlit as st

GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"

st.set_page_config(page_title="PookieBear", page_icon="💗", layout="centered")

# -----------------------------
# CSS: clean, pink/white, real animations, real SVG cats
# -----------------------------
st.markdown(
    """
<style>
/* --- Reset Streamlit spacing --- */
.block-container { max-width: 760px; padding-top: 34px; }
#MainMenu, footer, header { visibility: hidden; }

/* --- Fonts --- */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');
html, body, [class*="css"]  { font-family: Manrope, system-ui, -apple-system, Segoe UI, Roboto, Arial; }

/* --- Theme vars --- */
:root{
  --bg1:#fff7fb;
  --bg2:#ffeaf3;
  --pink:#ff3f9c;
  --pink2:#ff78bd;
  --ink:#241a22;
  --muted:#6f5f6a;
  --card:#ffffffcc;
  --border: rgba(255, 63, 156, 0.14);
  --shadow: 0 26px 70px rgba(255, 63, 156, 0.14);
}

/* --- Background --- */
.stApp{
  background: radial-gradient(1200px 700px at 15% 10%, #ffe1ef 0%, transparent 60%),
              radial-gradient(900px 650px at 90% 25%, #ffeef6 0%, transparent 62%),
              linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 60%, #ffffff 100%);
}

/* --- Animated blobs --- */
@keyframes drift {
  0%   { transform: translate3d(0,0,0) scale(1); }
  50%  { transform: translate3d(22px,-18px,0) scale(1.06); }
  100% { transform: translate3d(0,0,0) scale(1); }
}
.blob {
  position: fixed;
  width: 520px;
  height: 520px;
  border-radius: 999px;
  filter: blur(32px);
  opacity: 0.55;
  z-index: 0;
  animation: drift 10s ease-in-out infinite;
}
.blob.one { left: -220px; top: -200px; background: radial-gradient(circle, #ffb6d7 0%, transparent 62%); }
.blob.two { right: -260px; top: 40px; background: radial-gradient(circle, #ffd2e7 0%, transparent 62%); animation-duration: 12s; }
.blob.three{ left: 30%; bottom: -320px; background: radial-gradient(circle, #ffc0dd 0%, transparent 62%); animation-duration: 14s; }

/* --- Card layout --- */
.shell { position: relative; z-index: 2; }
.card{
  position: relative;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 26px;
  padding: 28px;
  box-shadow: var(--shadow);
  overflow: hidden;
  backdrop-filter: blur(10px);
}
.card::before{
  content:"";
  position:absolute; inset:-2px;
  background: radial-gradient(520px 180px at 15% 0%, rgba(255, 63, 156, 0.16), transparent 60%),
              radial-gradient(420px 160px at 92% 20%, rgba(255, 120, 189, 0.12), transparent 60%);
  pointer-events:none;
}

/* --- Header --- */
.toprow{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 14px;
  margin-bottom: 14px;
}
.brand{
  display:flex; align-items:center; gap:10px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -0.4px;
}
.pill{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 63, 156, 0.18);
  background: rgba(255,255,255,0.75);
  color: var(--muted);
}
.title{
  font-size: 40px;
  line-height: 1.06;
  letter-spacing: -1.1px;
  color: var(--ink);
  margin: 6px 0 10px 0;
}
.subtitle{
  font-size: 16px;
  line-height: 1.55;
  color: var(--muted);
  margin: 0 0 18px 0;
}

/* --- Buttons (Streamlit) --- */
div.stButton > button{
  width: 100%;
  height: 60px;
  border-radius: 18px;
  font-size: 18px;
  font-weight: 800;
  border: 1px solid rgba(36,26,34,0.10);
  background: rgba(255,255,255,0.9);
  color: var(--ink);
  transition: transform .12s ease, box-shadow .12s ease;
  box-shadow: 0 14px 34px rgba(255, 63, 156, 0.10);
}
div.stButton > button:hover{
  transform: translateY(-1px);
  box-shadow: 0 18px 46px rgba(255, 63, 156, 0.16);
}
div.stButton > button:active{ transform: translateY(0px) scale(0.99); }

/* Primary YES */
.primary div.stButton > button{
  background: linear-gradient(135deg, var(--pink) 0%, var(--pink2) 100%) !important;
  color: white !important;
  border: none !important;
  height: 66px !important;
  font-size: 20px !important;
  box-shadow: 0 22px 60px rgba(255, 63, 156, 0.28) !important;
}
.primary div.stButton > button:hover{
  box-shadow: 0 26px 70px rgba(255, 63, 156, 0.34) !important;
}

/* Grid row */
.grid{
  display:grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
  margin-top: 6px;
}
.note{
  font-size: 13px;
  color: rgba(111,95,106,0.95);
  margin-top: 8px;
}

/* Cute cat SVG holder */
.catbadge{
  width:44px; height:44px;
  border-radius: 14px;
  border: 1px solid rgba(255, 63, 156, 0.16);
  background: rgba(255,255,255,0.8);
  display:flex; align-items:center; justify-content:center;
}
</style>

<div class="blob one"></div>
<div class="blob two"></div>
<div class="blob three"></div>
""",
    unsafe_allow_html=True,
)

CAT_SVG = """
<svg width="26" height="26" viewBox="0 0 24 24" fill="none">
  <path d="M6.3 10.2 4.4 6.6c-.2-.4.2-.9.7-.8l3.4.8M17.7 10.2l1.9-3.6c.2-.4-.2-.9-.7-.8l-3.4.8"
        stroke="#241a22" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M6.8 12.6c0-3.1 2.5-5.6 5.6-5.6s5.6 2.5 5.6 5.6v2.1c0 2.9-2.3 5.2-5.2 5.2h-.8c-2.9 0-5.2-2.3-5.2-5.2v-2.1Z"
        fill="white" stroke="#241a22" stroke-width="1.5"/>
  <circle cx="10" cy="13" r="1" fill="#241a22"/>
  <circle cx="14" cy="13" r="1" fill="#241a22"/>
  <path d="M12 14.4c.7 0 1.2.5 1.2 1.2S12.7 16.8 12 16.8 10.8 16.3 10.8 15.6 11.3 14.4 12 14.4Z"
        fill="#ff3f9c" opacity=".55"/>
  <path d="M8.2 15.5H6.3M8.3 16.7H6.5M15.8 15.5h1.9M15.7 16.7h1.8"
        stroke="#241a22" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>
</svg>
"""

# -----------------------------
# State
# -----------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "boot"

def boot_screen():
    st.markdown(
        f"""
<div class="shell">
  <div class="card">
    <div class="toprow">
      <div class="brand">
        <div class="catbadge">{CAT_SVG}</div>
        <div>PookieBear</div>
      </div>
      <div class="pill">valentine edition</div>
    </div>

    <div class="title">Loading something cute…</div>
    <div class="subtitle">Preparing one important question for <b>{GF_NAME}</b>.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    p = st.progress(0)
    for i in range(100):
        time.sleep(0.010)
        p.progress(i + 1)

    if st.button("Continue"):
        st.session_state.stage = "question"
        st.rerun()

def question_screen():
    st.markdown(
        f"""
<div class="shell">
  <div class="card">
    <div class="toprow">
      <div class="brand">
        <div class="catbadge">{CAT_SVG}</div>
        <div>PookieBear</div>
      </div>
      <div class="pill">pink • clean • serious</div>
    </div>

    <div class="title">{GF_NAME}, will you be my Valentine?</div>
    <div class="subtitle">No pressure. But the “no” option may behave… oddly.</div>

    <div class="grid">
      <div id="yes-slot"></div>
      <div id="no-slot"></div>
    </div>

    <div class="note">Tip: the “no” button is shy and refuses accountability.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Put YES button in first column (Streamlit)
    c1, c2 = st.columns([1.15, 0.85], gap="large")
    with c1:
        st.markdown('<div class="primary">', unsafe_allow_html=True)
        if st.button("Yes, be my Valentine"):
            st.session_state.stage = "yes"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        # Real moving NO button (JS), styled to match the card
        st.components.v1.html(
            """
<div style="
  position: relative;
  height: 76px;
  border-radius: 18px;
  border: 1px solid rgba(36,26,34,0.10);
  background: rgba(255,255,255,0.92);
  box-shadow: 0 14px 34px rgba(255, 63, 156, 0.10);
  overflow: hidden;
">
  <button id="noBtn" style="
    position:absolute;
    left: 18%;
    top: 10px;
    height: 56px;
    padding: 0 16px;
    border-radius: 16px;
    border: 1px solid rgba(255, 63, 156, 0.22);
    background: rgba(255, 63, 156, 0.08);
    font-family: Manrope, system-ui, -apple-system, Segoe UI, Roboto, Arial;
    font-weight: 800;
    font-size: 16px;
    color: rgba(36,26,34,0.92);
    cursor: pointer;
    transition: transform .12s ease, opacity .18s ease, filter .18s ease;
  ">No</button>

  <div id="status" style="
    position:absolute; left:12px; bottom:8px;
    font-family: Manrope, system-ui, -apple-system, Segoe UI, Roboto, Arial;
    font-size: 12px; color: rgba(111,95,106,0.95);
  ">Hover to try.</div>
</div>

<script>
(function(){
  const btn = document.getElementById("noBtn");
  const status = document.getElementById("status");
  let tries = 0;

  function clamp(n,a,b){ return Math.max(a, Math.min(b, n)); }
  function rand(min,max){ return Math.random()*(max-min)+min; }

  function move(){
    // keep inside container
    const x = rand(8, 62);  // percent
    btn.style.left = x + "%";
    btn.style.top  = "10px";
  }

  function setText(){
    const t = [
      "Not today.",
      "Nope.",
      "That’s not available.",
      "Please choose the other button.",
      "This option has left the chat."
    ];
    status.textContent = t[Math.min(tries, t.length-1)];
  }

  function escalate(){
    // progressively harder to click
    if(tries === 1){
      btn.textContent = "Nope";
      btn.style.transform = "scale(0.92)";
    } else if(tries === 2){
      btn.textContent = "Still no";
      btn.style.transform = "scale(0.84) rotate(-2deg)";
    } else if(tries === 3){
      btn.textContent = "…";
      btn.style.filter = "blur(1.2px)";
      btn.style.transform = "scale(0.76) rotate(2deg)";
    } else if(tries === 4){
      btn.style.opacity = "0.45";
      btn.style.transform = "scale(0.68)";
      btn.textContent = "";
    } else if(tries >= 5){
      btn.style.opacity = "0";
      btn.style.pointerEvents = "none";
    }
  }

  btn.addEventListener("mouseenter", ()=>{
    tries = clamp(tries + 1, 0, 99);
    move(); setText(); escalate();
  });

  btn.addEventListener("click", ()=>{
    tries = clamp(tries + 2, 0, 99);
    move(); setText(); escalate();
  });

  setTimeout(move, 200);
})();
</script>
""",
            height=92,
        )

def yes_screen():
    st.markdown(
        f"""
<div class="shell">
  <div class="card">
    <div class="toprow">
      <div class="brand">
        <div class="catbadge">{CAT_SVG}</div>
        <div>PookieBear</div>
      </div>
      <div class="pill">confirmed</div>
    </div>

    <div class="title">It’s a yes.</div>
    <div class="subtitle"><b>{GF_NAME}</b> just made <b>{YOUR_NAME}</b> extremely happy.</div>

    <div style="
      margin-top: 16px;
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid rgba(255, 63, 156, 0.16);
      background: rgba(255, 255, 255, 0.86);
      color: rgba(36,26,34,0.92);
      font-weight: 700;
    ">
      Feb 14 • all day • you + me
    </div>

    <div class="note" style="margin-top:14px;">Send me a screenshot.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("Replay"):
        st.session_state.stage = "boot"
        st.rerun()

# -----------------------------
# Router
# -----------------------------
if st.session_state.stage == "boot":
    boot_screen()
elif st.session_state.stage == "question":
    question_screen()
else:
    yes_screen()
