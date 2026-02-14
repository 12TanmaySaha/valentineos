import random
import time
import streamlit as st

# -----------------------------
# Customize
# -----------------------------
GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="PookieBear Experience", page_icon="🐾", layout="centered")

# -----------------------------
# CSS: pink/white, clean, premium
# -----------------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container{max-width:820px; padding-top:26px; padding-bottom:40px;}

:root{
  --bg1:#fff7fb;
  --bg2:#ffe6f1;
  --card: rgba(255,255,255,0.82);
  --stroke: rgba(255, 63, 156, 0.16);
  --ink: #241a22;
  --muted:#6f5f6a;
  --pink:#ff3f9c;
  --pink2:#ff78bd;
  --shadow: 0 26px 70px rgba(255, 63, 156, 0.14);
}

.stApp{
  background:
    radial-gradient(1200px 700px at 12% 8%, #ffe1ef 0%, transparent 60%),
    radial-gradient(900px 650px at 92% 22%, #ffeef6 0%, transparent 62%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 60%, #ffffff 100%);
}

@keyframes drift{
  0%{ transform: translate3d(0,0,0) scale(1); }
  50%{ transform: translate3d(18px,-14px,0) scale(1.05); }
  100%{ transform: translate3d(0,0,0) scale(1); }
}
.blob{
  position: fixed;
  width: 520px; height: 520px;
  border-radius: 999px;
  filter: blur(32px);
  opacity: .55;
  z-index: 0;
  pointer-events:none;
  animation: drift 11s ease-in-out infinite;
}
.b1{ left:-240px; top:-260px; background: radial-gradient(circle, #ffb6d7 0%, transparent 62%); }
.b2{ right:-280px; top:10px; background: radial-gradient(circle, #ffd2e7 0%, transparent 62%); animation-duration: 13s; }
.b3{ left:28%; bottom:-340px; background: radial-gradient(circle, #ffc0dd 0%, transparent 62%); animation-duration: 15s; }

.shell{position:relative; z-index:2;}
.card{
  border-radius: 26px;
  border: 1px solid var(--stroke);
  background: var(--card);
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
  overflow:hidden;
}
.pad{padding:26px;}
.toprow{display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:12px;}
.brand{display:flex; align-items:center; gap:12px; font-weight:900; letter-spacing:-.4px; color:var(--ink);}
.pill{
  font-size:12px; padding:6px 10px; border-radius:999px;
  border:1px solid rgba(255,63,156,0.18);
  background: rgba(255,255,255,0.78);
  color: var(--muted);
  white-space:nowrap;
}
.title{font-size: 40px; line-height:1.06; letter-spacing:-1.1px; margin:8px 0 10px; color:var(--ink);}
.subtitle{font-size:16px; line-height:1.6; margin:0 0 16px; color:var(--muted);}

.stepper{
  display:flex; gap:8px; align-items:center; flex-wrap:wrap;
  margin-top:10px;
}
.stepDot{
  width:10px; height:10px; border-radius:999px;
  background: rgba(36,26,34,0.12);
}
.stepDot.on{ background: linear-gradient(135deg, var(--pink), var(--pink2)); }
.stepLabel{font-size:12px; color:var(--muted); margin-left:8px;}

.kpiRow{display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-top:14px;}
.kpi{
  border-radius: 18px;
  border: 1px solid rgba(255,63,156,0.12);
  background: rgba(255,255,255,0.78);
  padding: 12px;
}
.kpi .k{font-size:12px; color:var(--muted);}
.kpi .v{font-size:16px; font-weight:900; color:var(--ink); margin-top:2px;}

.divider{height:1px; background: rgba(255,63,156,0.12); margin:18px 0;}

.small{font-size:13px; color: rgba(111,95,106,0.95);}

/* Streamlit buttons */
div.stButton > button, button[kind="primary"]{
  width:100%;
  height:58px;
  border-radius:18px !important;
  font-size:18px !important;
  font-weight:900 !important;
  border: 1px solid rgba(36,26,34,0.10) !important;
  background: rgba(255,255,255,0.92) !important;
  color: var(--ink) !important;
  box-shadow: 0 14px 34px rgba(255,63,156,0.10) !important;
  transition: transform .12s ease, box-shadow .12s ease !important;
}
div.stButton > button:hover{
  transform: translateY(-1px);
  box-shadow: 0 18px 46px rgba(255,63,156,0.16) !important;
}
div.stButton > button:active{
  transform: translateY(0px) scale(0.99);
}

/* Primary CTA wrapper */
.primaryWrap div.stButton > button{
  border:none !important;
  color:white !important;
  background: linear-gradient(135deg, var(--pink) 0%, var(--pink2) 100%) !important;
  height:64px !important;
  font-size:20px !important;
  box-shadow: 0 22px 60px rgba(255,63,156,0.28) !important;
}
.primaryWrap div.stButton > button:hover{
  box-shadow: 0 26px 72px rgba(255,63,156,0.34) !important;
}

/* Inputs */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stRadio div[role="radiogroup"]{
  border-radius:16px !important;
}
</style>

<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
""", unsafe_allow_html=True)

# -----------------------------
# SVG cat icon (clean, not emoji)
# -----------------------------
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
# Stable state machine
# -----------------------------
STEPS = ["Boot", "Pookie Passport", "Compatibility", "Pinky Promise", "Final Question"]

def init_state():
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("passport", {"nickname": "", "fav_snack": "", "fav_color": "", "vibe": ""})
    st.session_state.setdefault("quiz", {"score": 0, "done": False})
    st.session_state.setdefault("promise", {"ideas": []})
    st.session_state.setdefault("final_yes", False)
    st.session_state.setdefault("seed", random.randint(1, 999999))

def go(step_idx: int):
    st.session_state.step = max(0, min(step_idx, len(STEPS) - 1))
    st.rerun()

def stepper():
    dots = []
    for i in range(len(STEPS)):
        cls = "stepDot on" if i <= st.session_state.step else "stepDot"
        dots.append(f"<span class='{cls}'></span>")
    st.markdown(
        f"<div class='stepper'>{''.join(dots)}"
        f"<span class='stepLabel'>{STEPS[st.session_state.step]} ({st.session_state.step+1}/{len(STEPS)})</span></div>",
        unsafe_allow_html=True
    )
    st.progress((st.session_state.step + 1) / len(STEPS))

def header(title: str, subtitle: str, pill: str):
    st.markdown(f"""
<div class="shell">
  <div class="card">
    <div class="pad">
      <div class="toprow">
        <div class="brand">
          <div style="width:44px;height:44px;border-radius:14px;border:1px solid rgba(255,63,156,0.16);
                      background:rgba(255,255,255,0.82);display:grid;place-items:center;">{CAT_SVG}</div>
          <div>PookieBear</div>
        </div>
        <div class="pill">{pill}</div>
      </div>

      <div class="title">{title}</div>
      <div class="subtitle">{subtitle}</div>
      {"<div class='divider'></div>" if st.session_state.step > 0 else ""}
""", unsafe_allow_html=True)
    stepper()

def footer_nav(show_back=True, show_next=True, next_label="Next"):
    c1, c2 = st.columns(2, gap="large")
    with c1:
        if show_back:
            if st.button("Back"):
                go(st.session_state.step - 1)
    with c2:
        if show_next:
            if st.button(next_label):
                go(st.session_state.step + 1)

def close_card():
    st.markdown("</div></div></div>", unsafe_allow_html=True)

# -----------------------------
# Screens
# -----------------------------
init_state()

# STEP 1: Boot
if st.session_state.step == 0:
    header(
        title="A small experience, for one person.",
        subtitle=f"This is a private little app designed for <b>{GF_NAME}</b>. "
                 f"It takes ~60 seconds and ends with one question.",
        pill="pink • clean • safe"
    )
    close_card()

    st.markdown("<div class='small'>Loading modules…</div>", unsafe_allow_html=True)
    p = st.progress(0)
    for i in range(100):
        time.sleep(0.008)
        p.progress(i + 1)

    st.markdown("<div class='kpiRow'>"
                "<div class='kpi'><div class='k'>Vibe</div><div class='v'>Soft</div></div>"
                "<div class='kpi'><div class='k'>Theme</div><div class='v'>Pink / White</div></div>"
                "<div class='kpi'><div class='k'>Outcome</div><div class='v'>Happiness</div></div>"
                "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="primaryWrap">', unsafe_allow_html=True)
    if st.button("Start"):
        go(1)
    st.markdown("</div>", unsafe_allow_html=True)

# STEP 2: Passport
elif st.session_state.step == 1:
    header(
        title="Pookie Passport",
        subtitle="Tiny details, but they make it feel personal. Fill these quickly (or skip with anything).",
        pill="step 2"
    )

    with st.form("passport_form", clear_on_submit=False):
        nickname = st.text_input("What do I call you?", value=st.session_state.passport["nickname"], placeholder="e.g., pookie / baby / Dipika")
        snack = st.text_input("Your comfort snack", value=st.session_state.passport["fav_snack"], placeholder="e.g., chocolate / chips / ice cream")
        color = st.selectbox("Your favorite color", ["", "Pink", "White", "Black", "Blue", "Purple", "Red", "Green", "Other"],
                             index=0 if st.session_state.passport["fav_color"] == "" else
                             ["", "Pink", "White", "Black", "Blue", "Purple", "Red", "Green", "Other"].index(st.session_state.passport["fav_color"]))
        vibe = st.selectbox("Today’s vibe", ["", "Soft", "Cute", "Elegant", "Chaotic", "Sleepy", "Romantic"],
                            index=0 if st.session_state.passport["vibe"] == "" else
                            ["", "Soft", "Cute", "Elegant", "Chaotic", "Sleepy", "Romantic"].index(st.session_state.passport["vibe"]))
        submitted = st.form_submit_button("Save passport")

    if submitted:
        st.session_state.passport = {"nickname": nickname.strip(), "fav_snack": snack.strip(), "fav_color": color, "vibe": vibe}
        st.success("Saved.")

    close_card()

    footer_nav(show_back=True, show_next=True, next_label="Continue")

# STEP 3: Compatibility quiz (longer, polished)
elif st.session_state.step == 2:
    header(
        title="Compatibility Check",
        subtitle="This is not science. This is pookie logic. Answer 4 quick questions.",
        pill="step 3"
    )

    if not st.session_state.quiz["done"]:
        with st.form("quiz_form"):
            q1 = st.radio("Pick a date style", ["Cozy café", "Movie night", "Walk + photos", "Fancy dinner"], index=0)
            q2 = st.radio("Pick a gift vibe", ["Handwritten note", "Chocolate", "Flowers", "A surprise plan"], index=0)
            q3 = st.radio("Pick a music mood", ["Soft + calm", "Pop", "Bollywood", "Anything if it's together"], index=0)
            q4 = st.radio("Pick a pet energy", ["Cat energy", "Golden retriever energy", "Both", "Sleepy panda"], index=0)
            done = st.form_submit_button("Calculate score")

        if done:
            # simple deterministic scoring (bug-safe, no random surprises)
            score = 70
            if q1 in ["Cozy café", "Movie night"]:
                score += 10
            if q2 in ["Handwritten note", "A surprise plan"]:
                score += 10
            if q3 == "Anything if it's together":
                score += 10
            if q4 == "Cat energy":
                score += 10
            score = min(score, 100)

            st.session_state.quiz = {"score": score, "done": True}
            st.rerun()

    else:
        score = st.session_state.quiz["score"]
        st.markdown(f"<div class='kpiRow'>"
                    f"<div class='kpi'><div class='k'>Compatibility</div><div class='v'>{score}%</div></div>"
                    f"<div class='kpi'><div class='k'>Risk</div><div class='v'>Falling harder</div></div>"
                    f"<div class='kpi'><div class='k'>Verdict</div><div class='v'>Approved</div></div>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        nick = st.session_state.passport.get("nickname") or GF_NAME
        snack = st.session_state.passport.get("fav_snack") or "something sweet"
        st.info(f"Result: {nick} + {YOUR_NAME} = dangerous levels of cute. Reward: {snack}.")

        if st.button("Recalculate (just for fun)"):
            st.session_state.quiz = {"score": 0, "done": False}
            st.rerun()

    close_card()
    footer_nav(show_back=True, show_next=True, next_label="Continue")

# STEP 4: Pinky Promise (longer)
elif st.session_state.step == 3:
    header(
        title="Pinky Promise",
        subtitle="Pick what you want on Valentine’s. I’ll treat it like a contract.",
        pill="step 4"
    )

    ideas = st.multiselect(
        "Choose your perfect plan",
        ["Café + dessert", "Flowers", "Movie night", "Walk + photos", "A surprise itinerary", "Stay in + cozy night", "Fancy dinner"],
        default=st.session_state.promise["ideas"],
    )
    st.session_state.promise["ideas"] = ideas

    nick = st.session_state.passport.get("nickname") or GF_NAME
    vibe = st.session_state.passport.get("vibe") or "Soft"
    color = st.session_state.passport.get("fav_color") or "Pink"

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='small'><b>Pookie Contract</b><br>"
        f"I, <b>{YOUR_NAME}</b>, agree to deliver a <b>{vibe}</b> day for <b>{nick}</b>.<br>"
        f"Theme: <b>{color}</b>. Chosen plan: <b>{', '.join(ideas) if ideas else 'to be decided together'}</b>.</div>",
        unsafe_allow_html=True
    )

    close_card()
    footer_nav(show_back=True, show_next=True, next_label="Continue")

# STEP 5: Final Question (best part)
else:
    nick = st.session_state.passport.get("nickname") or GF_NAME

    header(
        title=f"{nick}, one last screen.",
        subtitle="This is the actual question. The rest was just to make you smile.",
        pill="final"
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='title' style='font-size:34px;margin-top:0'>Will you be my Valentine?</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='small'>The “no” button has… opinions.</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 0.75], gap="large")
    with left:
        st.markdown('<div class="primaryWrap">', unsafe_allow_html=True)
        if st.button("Yes, I will"):
            st.session_state.final_yes = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='small'>Clicking yes triggers the official confirmation card.</div>", unsafe_allow_html=True)

    with right:
        # Escaping NO button (JS). This is stable and self-contained.
        st.components.v1.html(
            """
<div style="
  height: 120px;
  border-radius: 18px;
  border: 1px solid rgba(36,26,34,0.10);
  background: rgba(255,255,255,0.92);
  box-shadow: 0 14px 34px rgba(255,63,156,0.10);
  position: relative;
  overflow:hidden;
  padding: 14px;
">
  <div style="font-weight:900; color: rgba(36,26,34,0.86); margin-bottom:10px;">No (if you can)</div>
  <button id="noBtn" style="
    position:absolute; left: 18%; top: 56px;
    height: 44px; padding: 0 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,63,156,0.22);
    background: rgba(255,63,156,0.08);
    font-weight: 900; font-size: 14px;
    color: rgba(36,26,34,0.92);
    cursor: pointer;
    transition: transform .12s ease, opacity .18s ease, filter .18s ease;
    will-change: left, transform, opacity;
  ">No</button>

  <div id="msg" style="
    position:absolute; left:14px; bottom:10px;
    font-size:12px; color: rgba(111,95,106,0.95);
  ">Hover near it.</div>
</div>

<script>
(function(){
  const btn = document.getElementById("noBtn");
  const msg = document.getElementById("msg");
  let t = 0;

  function clamp(n,a,b){ return Math.max(a, Math.min(b,n)); }
  function rand(min,max){ return Math.random()*(max-min)+min; }

  function move(){
    const x = rand(8, 70);
    btn.style.left = x + "%";
  }
  function setMsg(){
    const lines = [
      "No is under maintenance.",
      "Nice try.",
      "It’s shy.",
      "Please press yes.",
      "Option removed."
    ];
    msg.textContent = lines[Math.min(t, lines.length-1)];
  }
  function escalate(){
    if(t===1){ btn.textContent="Nope"; btn.style.transform="scale(0.92)"; }
    else if(t===2){ btn.textContent="…"; btn.style.transform="scale(0.84) rotate(-2deg)"; }
    else if(t===3){ btn.style.filter="blur(1.2px)"; btn.style.transform="scale(0.76) rotate(2deg)"; }
    else if(t===4){ btn.style.opacity="0.45"; btn.style.transform="scale(0.68)"; btn.textContent=""; }
    else if(t>=5){ btn.style.opacity="0"; btn.style.pointerEvents="none"; msg.textContent="No option has left."; }
  }

  // run away when mouse gets close
  const box = btn.parentElement;
  box.addEventListener("mousemove", (e)=>{
    if(btn.style.pointerEvents==="none") return;
    const r = btn.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width/2);
    const dy = e.clientY - (r.top + r.height/2);
    const d = Math.sqrt(dx*dx + dy*dy);
    if(d < 70){
      t = clamp(t+1, 0, 99);
      move(); setMsg(); escalate();
    }
  });

  btn.addEventListener("click", ()=>{
    t = clamp(t+2, 0, 99);
    move(); setMsg(); escalate();
  });

  setTimeout(move, 200);
})();
</script>
""",
            height=140,
        )

    close_card()

    # YES result card (Streamlit-only, stable)
    if st.session_state.final_yes:
        st.balloons()
        ideas = st.session_state.promise.get("ideas") or []
        plan = ", ".join(ideas) if ideas else "to be decided together"
        snack = st.session_state.passport.get("fav_snack") or "something sweet"

        st.markdown(f"""
<div class="shell">
  <div class="card">
    <div class="pad">
      <div class="toprow">
        <div class="brand">
          <div style="width:44px;height:44px;border-radius:14px;border:1px solid rgba(255,63,156,0.16);
                      background:rgba(255,255,255,0.82);display:grid;place-items:center;">{CAT_SVG}</div>
          <div>PookieBear</div>
        </div>
        <div class="pill">confirmed</div>
      </div>

      <div class="title" style="font-size:36px">It’s official.</div>
      <div class="subtitle"><b>{GF_NAME}</b> just made <b>{YOUR_NAME}</b> extremely happy.</div>

      <div class="kpiRow">
        <div class="kpi"><div class="k">Date</div><div class="v">Feb 14</div></div>
        <div class="kpi"><div class="k">Plan</div><div class="v">{plan}</div></div>
        <div class="kpi"><div class="k">Bonus</div><div class="v">{snack}</div></div>
      </div>

      <div class="divider"></div>
      <div class="small">Send me a screenshot of this screen.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("Replay the whole experience"):
                # reset cleanly (bug-free)
                for k in ["step", "passport", "quiz", "promise", "final_yes", "seed"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
        with c2:
            if st.button("Just go back"):
                st.session_state.final_yes = False
                go(4)
