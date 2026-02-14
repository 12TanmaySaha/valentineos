import time
import streamlit as st

GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"

st.set_page_config(page_title="PookieBear", page_icon="💗", layout="centered")

# -----------------------------
# Global CSS: pink/white, professional, real animations
# -----------------------------
st.markdown(
    """
<style>
/* Page background */
.stApp{
  background: radial-gradient(1200px 800px at 20% 10%, #ffe6f1 0%, transparent 55%),
              radial-gradient(900px 700px at 90% 30%, #fff1f7 0%, transparent 60%),
              linear-gradient(180deg, #ffffff 0%, #fff6fa 45%, #ffeaf3 100%);
}

/* Subtle animated shimmer */
@keyframes shimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.shimmer {
  background: linear-gradient(120deg, rgba(255,105,180,.10), rgba(255,255,255,0), rgba(255,105,180,.10));
  background-size: 200% 200%;
  animation: shimmer 8s ease-in-out infinite;
}

/* Typography */
:root{
  --pink:#ff4fa3;
  --pink2:#ff78b9;
  --text:#2a2430;
  --muted:#6f6477;
  --card:#ffffffcc;
  --border:#f3c4d9;
}
h1,h2,h3,p,div,span,button,input{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; }
a { color: var(--pink); }

/* Main card */
.card{
  position: relative;
  border: 1px solid rgba(243,196,217,.8);
  background: var(--card);
  border-radius: 26px;
  padding: 26px;
  box-shadow: 0 22px 60px rgba(255, 79, 163, 0.14);
  overflow: hidden;
}
.card::before{
  content:"";
  position:absolute; inset:-2px;
  border-radius: 28px;
  background: radial-gradient(400px 140px at 20% 0%, rgba(255,79,163,.18), transparent 60%),
              radial-gradient(380px 160px at 90% 20%, rgba(255,120,185,.14), transparent 60%);
  pointer-events:none;
}

/* Header */
.brand{
  display:flex; align-items:center; gap:10px;
  font-weight: 800; letter-spacing: -0.4px;
  color: var(--text);
}
.badge{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(243,196,217,.9);
  background: rgba(255,255,255,.65);
  color: var(--muted);
}
.title{
  font-size: 40px;
  line-height: 1.05;
  margin: 14px 0 6px 0;
  letter-spacing: -1px;
  color: var(--text);
}
.subtitle{
  font-size: 16px;
  margin: 0 0 14px 0;
  color: var(--muted);
}

/* Buttons: override Streamlit */
div.stButton > button{
  width: 100%;
  height: 58px;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 800;
  border: 1px solid rgba(243,196,217,.95);
  background: rgba(255,255,255,.9);
  color: var(--text);
  transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
  box-shadow: 0 10px 26px rgba(255, 79, 163, 0.10);
}
div.stButton > button:hover{
  transform: translateY(-1px);
  background: rgba(255,255,255,1);
  box-shadow: 0 14px 34px rgba(255, 79, 163, 0.16);
}
div.stButton > button:active{
  transform: translateY(0px) scale(0.99);
}

/* Primary YES button (bigger, professional) */
.primaryWrap div.stButton > button{
  background: linear-gradient(135deg, var(--pink) 0%, var(--pink2) 100%) !important;
  color: white !important;
  border: none !important;
  height: 64px !important;
  font-size: 20px !important;
  box-shadow: 0 18px 44px rgba(255, 79, 163, 0.28) !important;
}
.primaryWrap div.stButton > button:hover{
  box-shadow: 0 22px 56px rgba(255, 79, 163, 0.34) !important;
}

/* Cat bubbles (real CSS animation, no emoji spam) */
@keyframes floatUp {
  0%   { transform: translateY(40px) translateX(0) scale(0.95); opacity: 0; }
  15%  { opacity: .85; }
  100% { transform: translateY(-520px) translateX(18px) scale(1.10); opacity: 0; }
}
.catBubble{
  position: fixed;
  bottom: -60px;
  width: 54px;
  height: 54px;
  border-radius: 999px;
  background: rgba(255, 79, 163, 0.10);
  border: 1px solid rgba(255, 79, 163, 0.18);
  box-shadow: 0 18px 40px rgba(255, 79, 163, 0.10);
  display:flex; align-items:center; justify-content:center;
  animation: floatUp linear infinite;
  z-index: 0;
  backdrop-filter: blur(4px);
}
.catFace{
  width: 22px; height: 18px; position: relative;
  border-radius: 10px;
  border: 2px solid rgba(42,36,48,.45);
  background: rgba(255,255,255,.9);
}
.catEarL,.catEarR{
  position:absolute; top:-8px; width:10px; height:10px;
  background: rgba(255,255,255,.9);
  border-left:2px solid rgba(42,36,48,.45);
  border-top:2px solid rgba(42,36,48,.45);
  transform: rotate(45deg);
}
.catEarL{ left:2px; }
.catEarR{ right:2px; }
.catEyeL,.catEyeR{
  position:absolute; top:6px; width:4px; height:4px;
  background: rgba(42,36,48,.55); border-radius: 999px;
}
.catEyeL{ left:6px; }
.catEyeR{ right:6px; }
.catNose{
  position:absolute; top:10px; left:50%;
  width:6px; height:4px; transform: translateX(-50%);
  background: rgba(255, 79, 163, .55);
  border-radius: 2px 2px 6px 6px;
}
.catWhL,.catWhR{
  position:absolute; top:10px; width:10px; height:1px;
  background: rgba(42,36,48,.35);
}
.catWhL{ left:-10px; transform: rotate(8deg); }
.catWhR{ right:-10px; transform: rotate(-8deg); }

/* Keep everything above bubbles */
.block-container{ position: relative; z-index: 2; max-width: 720px; padding-top: 26px; }
</style>

<!-- Cat bubbles: few, classy, animated -->
<div class="catBubble" style="left: 8%; animation-duration: 10s; animation-delay: 0s;">
  <div class="catFace">
    <div class="catEarL"></div><div class="catEarR"></div>
    <div class="catEyeL"></div><div class="catEyeR"></div>
    <div class="catNose"></div><div class="catWhL"></div><div class="catWhR"></div>
  </div>
</div>
<div class="catBubble" style="left: 22%; animation-duration: 12s; animation-delay: 2s;">
  <div class="catFace">
    <div class="catEarL"></div><div class="catEarR"></div>
    <div class="catEyeL"></div><div class="catEyeR"></div>
    <div class="catNose"></div><div class="catWhL"></div><div class="catWhR"></div>
  </div>
</div>
<div class="catBubble" style="left: 65%; animation-duration: 11s; animation-delay: 1s;">
  <div class="catFace">
    <div class="catEarL"></div><div class="catEarR"></div>
    <div class="catEyeL"></div><div class="catEyeR"></div>
    <div class="catNose"></div><div class="catWhL"></div><div class="catWhR"></div>
  </div>
</div>
<div class="catBubble" style="left: 82%; animation-duration: 13s; animation-delay: 3s;">
  <div class="catFace">
    <div class="catEarL"></div><div class="catEarR"></div>
    <div class="catEyeL"></div><div class="catEyeR"></div>
    <div class="catNose"></div><div class="catWhL"></div><div class="catWhR"></div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# State
# -----------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "boot"
if "no_count" not in st.session_state:
    st.session_state.no_count = 0


def boot_screen():
    st.markdown(
        f"""
<div class="card shimmer">
  <div class="brand">
    <div style="font-size:18px;">PookieBear</div>
    <span class="badge">valentine edition</span>
  </div>
  <div class="title">Loading something cute…</div>
  <p class="subtitle">Preparing one important question for <b>{GF_NAME}</b>.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    p = st.progress(0)
    for i in range(100):
        time.sleep(0.012)
        p.progress(i + 1)

    if st.button("Continue"):
        st.session_state.stage = "question"
        st.rerun()


def question_screen():
    st.markdown(
        f"""
<div class="card">
  <div class="brand">
    <div style="font-size:18px;">PookieBear</div>
    <span class="badge">secure • cute • serious</span>
  </div>
  <div class="title">{GF_NAME}, will you be my Valentine?</div>
  <p class="subtitle">Be honest. But also… choose wisely.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # Layout: Big YES + interactive NO (escaping button)
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown('<div class="primaryWrap">', unsafe_allow_html=True)
        if st.button("Yes"):
            st.session_state.stage = "yes"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("This is the correct option.")

    with c2:
        # Escaping NO button with more “creative” behaviors
        # NOTE: This is front-end only; it’s meant for the gag.
        st.components.v1.html(
            """
<div style="position:relative; height:170px; border-radius:18px; background:rgba(255,255,255,.8);
            border:1px solid rgba(243,196,217,.95); box-shadow:0 10px 26px rgba(255,79,163,.10);
            overflow:hidden; padding:14px;">
  <div style="font-weight:800; color:rgba(42,36,48,.80); margin-bottom:10px;">Or… this one (if you can catch it)</div>
  <button id="noBtn"
    style="
      position:absolute;
      left: 30%;
      top: 55%;
      padding: 14px 18px;
      font-size: 16px;
      font-weight: 800;
      border-radius: 14px;
      border: 1px solid rgba(243,196,217,.95);
      background: rgba(255, 200, 220, .55);
      color: rgba(42,36,48,.85);
      cursor: pointer;
      transition: transform .12s ease, opacity .18s ease, filter .18s ease;
    "
  >No</button>

  <div id="noMsg" style="position:absolute; left:14px; bottom:12px; font-size:13px; color:rgba(111,100,119,.95);">
    Hint: try hovering.
  </div>
</div>

<script>
(function(){
  const btn = document.getElementById("noBtn");
  const msg = document.getElementById("noMsg");
  let tries = 0;

  function clamp(n, a, b){ return Math.max(a, Math.min(b, n)); }

  function teleport(){
    const x = Math.random()*70 + 10;
    const y = Math.random()*55 + 25;
    btn.style.left = x + "%";
    btn.style.top  = y + "%";
  }

  function taunt(){
    const lines = [
      "Nice try.",
      "Too slow.",
      "That option is under maintenance.",
      "This button is for decoration.",
      "Try the other button."
    ];
    msg.textContent = lines[Math.min(tries, lines.length-1)];
  }

  function escalate(){
    // Escalation: shrink -> blur -> fade -> vanish
    if(tries === 1){
      btn.style.transform = "scale(0.92)";
      btn.textContent = "Nope";
    } else if(tries === 2){
      btn.style.transform = "scale(0.84) rotate(-2deg)";
      btn.textContent = "Still no";
    } else if(tries === 3){
      btn.style.filter = "blur(1.2px)";
      btn.style.transform = "scale(0.76) rotate(2deg)";
      btn.textContent = "??";
    } else if(tries === 4){
      btn.style.opacity = "0.55";
      btn.style.transform = "scale(0.68)";
      btn.textContent = "…";
      msg.textContent = "Ok, it’s getting shy.";
    } else if(tries >= 5){
      btn.style.opacity = "0";
      btn.style.pointerEvents = "none";
      msg.textContent = "No option has left the chat.";
    }
  }

  // Run away from cursor: also reacts to near-miss
  btn.addEventListener("mouseenter", ()=>{
    tries = clamp(tries + 1, 0, 99);
    teleport();
    taunt();
    escalate();
  });

  // If clicked, it panics harder
  btn.addEventListener("click", ()=>{
    tries = clamp(tries + 2, 0, 99);
    teleport();
    taunt();
    escalate();
  });

  // initial teleport so it feels alive
  setTimeout(teleport, 350);
})();
</script>
""",
            height=190,
        )


def yes_screen():
    st.balloons()
    st.markdown(
        f"""
<div class="card shimmer">
  <div class="brand">
    <div style="font-size:18px;">PookieBear</div>
    <span class="badge">confirmed</span>
  </div>
  <div class="title">Okay. That’s a yes.</div>
  <p class="subtitle"><b>{GF_NAME}</b> just made <b>{YOUR_NAME}</b> extremely happy.</p>

  <div style="margin-top:14px; padding:14px; border-radius:18px; background: rgba(255,255,255,.75);
              border:1px solid rgba(243,196,217,.95); color: rgba(42,36,48,.86);">
    Plan: Feb 14 • all day • you + me
  </div>

  <p class="subtitle" style="margin-top:14px;">Send me a screenshot 😌</p>
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
