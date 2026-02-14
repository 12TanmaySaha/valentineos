"""
Complete Streamlit Valentine App with Floating Hearts

This script is a cleaned‑up version of the original Valentine
certificate app you shared.  It preserves all of the original
features—floating hearts, cute boot screen, tiny details form,
compatibility quiz, plan picker, memory lane, the mischievous
“no” button and PDF certificate generation—while making some
practical fixes so it runs smoothly on Streamlit Community Cloud:

* `st.set_page_config` is called at the very top of the script,
  before any other Streamlit calls.  This avoids errors that can
  prevent the app from loading.
* The ReportLab import is deferred to the moment you generate the
  PDF.  If ReportLab isn’t installed, the rest of the app still
  runs; users will see an error only when they click the download
  button.
* All strings use plain quotes to avoid syntax issues.

To deploy this app on Streamlit Cloud or run locally, place this
file in your repository as `streamlit_app.py` (or configure the
deployment to point at this file) and include a `requirements.txt`
listing at least `streamlit` and `reportlab`.
"""

import time
import random
from io import BytesIO

import streamlit as st

# ---------------------------------------------------------------------------
# Initial configuration

# Configure the page right away.  Streamlit requires this to be the first
# Streamlit call.
st.set_page_config(page_title="💗 Valentine", page_icon="💗", layout="centered")

# Names for the certificate
GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"

# ---------------------------------------------------------------------------
# Theme and CSS

def inject_theme() -> None:
    """Inject the Valentine theme and floating hearts CSS."""
    st.markdown(
        """
        <style>
        /* Hide Streamlit default UI */
        #MainMenu, footer, header {visibility:hidden;}
        .block-container{max-width:860px; padding-top:22px; padding-bottom:44px;}

        :root{
          --bg:#fff7fb;
          --bg2:#ffe7f2;
          --card:rgba(255,255,255,0.86);
          --card2:rgba(255,255,255,0.72);
          --stroke:rgba(255, 78, 155, 0.16);
          --shadow: 0 26px 80px rgba(255, 78, 155, 0.14);
          --ink:#241a22;
          --muted:#6b5c66;
          --pink:#ff2f92;
          --pink2:#ff84c5;
          --cream:#fff0f7;
        }

        .stApp{
          background:
            radial-gradient(1200px 700px at 12% 8%, #ffd3e6 0%, transparent 62%),
            radial-gradient(900px 650px at 92% 22%, #fff1f8 0%, transparent 62%),
            linear-gradient(180deg, var(--bg) 0%, var(--bg2) 60%, #ffffff 100%);
        }

        /* Floating hearts animation */
        @keyframes floaty {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
          100% { transform: translateY(0px); }
        }
        @keyframes march {
          0% { transform: translateX(-120px) translateY(0px); opacity: 0; }
          10%{ opacity: 1;}
          50%{ transform: translateX(35vw) translateY(-6px); }
          100%{ transform: translateX(105vw) translateY(0px); opacity: 0; }
        }

        .grain{
          position: fixed; inset:0; pointer-events:none; z-index:0;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='.18'/%3E%3C/svg%3E");
          mix-blend-mode: multiply;
          opacity: .14;
        }

        .blob{
          position: fixed; width:560px; height:560px; border-radius:999px;
          filter: blur(40px); opacity:.52; z-index:0; pointer-events:none;
          animation: floaty 10s ease-in-out infinite;
        }
        .b1{ left:-280px; top:-280px; background: radial-gradient(circle, #ffb5d7 0%, transparent 62%); }
        .b2{ right:-320px; top:20px; background: radial-gradient(circle, #ffd6ea 0%, transparent 62%); animation-duration: 13s;}
        .b3{ left:28%; bottom:-360px; background: radial-gradient(circle, #ffc1dd 0%, transparent 62%); animation-duration: 15s;}

        .shell{position:relative; z-index:2;}
        .card{
          border-radius: 28px;
          border: 1px solid var(--stroke);
          background: var(--card);
          box-shadow: var(--shadow);
          backdrop-filter: blur(10px);
          overflow:hidden;
        }
        .pad{padding:24px;}
        .h1{
          font-size: 44px; letter-spacing:-1.2px; line-height:1.02;
          color:var(--ink); margin:6px 0 8px;
        }
        .sub{
          font-size: 16px; line-height:1.65; color:var(--muted); margin:0;
        }
        .chipRow{display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;}
        .chip{
          font-size:12px; padding:7px 10px; border-radius:999px;
          border:1px solid rgba(255,47,146,0.16);
          background: rgba(255,255,255,0.85);
          color:var(--muted);
        }
        .hr{height:1px; background:rgba(255,47,146,0.10); margin:18px 0;}
        .stepRow{display:flex; align-items:center; gap:8px; margin-top:14px;}
        .dot{width:10px; height:10px; border-radius:999px; background:rgba(36,26,34,.12);} 
        .dot.on{ background: linear-gradient(135deg, var(--pink), var(--pink2)); }
        .stepLabel{font-size:12px; color:var(--muted); margin-left:8px;}

        .kgrid{display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; margin-top:14px;}
        .k{
          border-radius: 18px; padding: 12px;
          border:1px solid rgba(255,47,146,0.12);
          background: rgba(255,255,255,0.86);
        }
        .k .t{font-size:12px; color:var(--muted);} 
        .k .v{font-size:16px; font-weight:900; color:var(--ink); margin-top:2px;}

        .bigBtn div.stButton > button{
          width:100%;
          height:64px;
          border-radius:18px !important;
          border:none !important;
          color:white !important;
          font-weight:900 !important;
          font-size:20px !important;
          background: linear-gradient(135deg, var(--pink) 0%, var(--pink2) 100%) !important;
          box-shadow: 0 22px 70px rgba(255,47,146,0.24) !important;
        }
        .bigBtn div.stButton > button:hover{ transform: translateY(-1px); }
        
        div.stButton > button{
          width:100%;
          height:54px;
          border-radius:16px !important;
          font-size:17px !important;
          font-weight:850 !important;
          border: 1px solid rgba(36,26,34,0.10) !important;
          background: rgba(255,255,255,0.96) !important;
          color: var(--ink) !important;
          box-shadow: 0 14px 34px rgba(255,47,146,0.10) !important;
        }
        div.stButton > button:hover{ transform: translateY(-1px); }

        label, .stMarkdown, .stText, p, span, div { color: var(--ink); }
        .stTextInput input, .stTextArea textarea{
          background: rgba(255,255,255,0.98) !important;
          color: var(--ink) !important;
          border-radius: 14px !important;
          border: 1px solid rgba(255,47,146,0.16) !important;
        }
        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div{
          background: rgba(255,255,255,0.98) !important;
          border-radius: 14px !important;
          border: 1px solid rgba(255,47,146,0.16) !important;
        }
        /* Fix the DARK dropdown (BaseWeb portal lives elsewhere) */
        div[data-baseweb="popover"]{
          background: rgba(255,255,255,0.98) !important;
          border-radius: 16px !important;
          border: 1px solid rgba(255,47,146,0.16) !important;
          box-shadow: 0 18px 60px rgba(255,47,146,0.18) !important;
        }
        div[data-baseweb="menu"]{
          background: rgba(255,255,255,0.98) !important;
        }
        div[data-baseweb="option"]{
          color: var(--ink) !important;
        }
        div[data-baseweb="option"]:hover{
          background: rgba(255,47,146,0.08) !important;
        }

        /* Cute background cat (CSS-only) */
        .bgcat{
          position: fixed;
          bottom: 24px;
          left: 0;
          z-index: 1;
          opacity: .34;
          animation: march 10s linear infinite;
          pointer-events:none;
        }
        .bgcat svg{ filter: drop-shadow(0 18px 26px rgba(255,47,146,0.18)); }

        .sparkle{
          position: absolute;
          right: 18px;
          top: 18px;
          width: 84px; height: 84px;
          opacity: .25;
          animation: floaty 7s ease-in-out infinite;
        }
        </style>
        
        <!-- Static background elements -->
        <div class="grain"></div>
        <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
        <div class="bgcat">
        <svg width="140" height="70" viewBox="0 0 140 70" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M26 43c0-13 10-23 23-23h24c13 0 23 10 23 23v2c0 10-8 18-18 18H62c-10 0-18-8-18-18v-2Z" fill="white" stroke="#241A22" stroke-width="2"/>
          <circle cx="55" cy="42" r="3" fill="#241A22"/>
          <circle cx="72" cy="42" r="3" fill="#241A22"/>
          <path d="M63 46c2 0 4 2 4 4s-2 4-4 4-4-2-4-4 2-4 4-4Z" fill="#FF2F92" opacity=".55"/>
          <path d="M48 29l-7-10c-1-2 1-4 3-3l12 4" stroke="#241A22" stroke-width="2" stroke-linecap="round"/>
          <path d="M78 29l7-10c1-2-1-4-3-3l-12 4" stroke="#241A22" stroke-width="2" stroke-linecap="round"/>
          <path d="M96 55c14-1 24-8 28-18" stroke="#FF2F92" stroke-width="6" stroke-linecap="round" opacity=".35"/>
        </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# State management

STEPS = ["Boot", "Tiny things", "Little quiz", "Pick a plan", "Memory lane", "Final"]

def init_state() -> None:
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("tiny", {"nickname":"", "snack":"", "color":"", "mood":""})
    st.session_state.setdefault("quiz", {"done": False, "score": 0, "answers": {}})
    st.session_state.setdefault("plan", [])
    st.session_state.setdefault("mem", {"first":"", "moment":"", "love":"", "saved": False})
    st.session_state.setdefault("yes", False)

def go(i: int) -> None:
    st.session_state.step = max(0, min(i, len(STEPS)-1))
    st.experimental_rerun()

def stepper() -> None:
    dots = []
    for i in range(len(STEPS)):
        dots.append(f"<span class='dot {'on' if i<=st.session_state.step else ''}'></span>")
    st.markdown(
        f"<div class='stepRow'>{''.join(dots)}"
        f"<span class='stepLabel'>{STEPS[st.session_state.step]} ({st.session_state.step+1}/{len(STEPS)})</span></div>",
        unsafe_allow_html=True
    )
    st.progress((st.session_state.step+1)/len(STEPS))

def card_open() -> None:
    st.markdown("<div class='shell'><div class='card'><div class='pad'>", unsafe_allow_html=True)

def card_close() -> None:
    st.markdown("</div></div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Letter and PDF helpers

def build_letter() -> str:
    t = st.session_state.tiny
    m = st.session_state.mem
    nick = (t["nickname"].strip() or GF_NAME)
    snack = (t["snack"].strip() or "something sweet")
    plan = ", ".join(st.session_state.plan) if st.session_state.plan else "something we decide together"
    first = (m["first"].strip() or "I remember thinking: yep… she’s special.")
    moment = (m["moment"].strip() or "one of those small moments that randomly makes me smile later.")
    love = (m["love"].strip() or "how easy it feels to be myself around you.")
    return (
        f"Hey {nick},\n\n"
        f"I made this because I wanted to do something cute for you — the kind of cute that's a little embarrassing, but in a good way.\n\n"
        f"I still remember my first impression: {first}\n"
        f"My favorite moment: {moment}\n"
        f"And one thing I genuinely love about you: {love}\n\n"
        f"For Valentine’s, I’m claiming you for a {plan} kind of day — and yes, there will be {snack}.\n\n"
        f"Okay now… serious question.\n\n"
        f"— {YOUR_NAME}"
    )

def make_pdf(letter_text: str) -> bytes:
    """Generate the PDF certificate.  ReportLab is imported here to avoid import errors at module load time."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        raise RuntimeError("ReportLab is required to generate the PDF. Please install reportlab in your environment.")
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    margin = 1.6*cm
    # Outer border
    c.setLineWidth(2)
    c.setStrokeColorRGB(1.0, 0.18, 0.57)
    c.roundRect(margin, margin, w-2*margin, h-2*margin, 18, stroke=1, fill=0)
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(0.14, 0.10, 0.13)
    c.drawCentredString(w/2, h-3.0*cm, "Valentine Certificate")
    # Subtitle
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.43, 0.37, 0.41)
    c.drawCentredString(w/2, h-3.8*cm, "handmade (by a slightly nervous boyfriend)")
    # Names
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.14, 0.10, 0.13)
    c.drawCentredString(w/2, h-5.2*cm, f"{YOUR_NAME}  ↔  {GF_NAME}")
    # Content box
    box_x = 2.2*cm
    box_y = 4.0*cm
    box_w = w-4.4*cm
    box_h = h-10.8*cm
    c.setLineWidth(1)
    c.setStrokeColorRGB(1.0, 0.55, 0.74)
    c.setFillColorRGB(1.0, 0.97, 0.99)
    c.roundRect(box_x, box_y, box_w, box_h, 14, stroke=1, fill=1)
    # Letter text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.14, 0.10, 0.13)
    lines = []
    for para in letter_text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w0 in words:
            trial = (cur + " " + w0).strip()
            if c.stringWidth(trial, "Helvetica", 11) <= box_w - 1.2*cm:
                cur = trial
            else:
                lines.append(cur)
                cur = w0
        if cur:
            lines.append(cur)
    x = box_x + 0.6*cm
    y = box_y + box_h - 0.9*cm
    for ln in lines:
        if y < box_y + 0.8*cm:
            break
        c.drawString(x, y, ln)
        y -= 14
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.43, 0.37, 0.41)
    c.drawCentredString(w/2, margin + 0.9*cm, "This document is legally binding in my heart. (And only there.)")
    c.showPage()
    c.save()
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Pages

def page_boot() -> None:
    card_open()
    st.markdown("<div class='sparkle'>✦</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='h1'>okay hi.</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='sub'>this is for <b>{GF_NAME}</b>. it’s short, cute, and slightly unfair to the “no” button.</p>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='chipRow'>"
                "<span class='chip'>compiling feelings…</span>"
                "<span class='chip'>linking cuddles…</span>"
                "<span class='chip'>optimizing hugs…</span>"
                "</div>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    msgs = [
        "checking if your smile is online… ✅",
        "warming up the cute stuff…",
        "loading tiny butterflies…",
        "setting the “no” button to hard mode…",
        "almost done. don’t blink."
    ]
    spot = st.empty()
    prog = st.progress(0)
    for i in range(100):
        if i % 18 == 0:
            spot.markdown(f"<div class='sub'>{random.choice(msgs)}</div>", unsafe_allow_html=True)
        time.sleep(0.01)
        prog.progress(i+1)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="bigBtn">', unsafe_allow_html=True)
    if st.button("start"):
        go(1)
    st.markdown("</div>", unsafe_allow_html=True)
    card_close()

def page_tiny() -> None:
    card_open()
    st.markdown("<div class='h1'>tiny things about you</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>nothing deep. just the cute details that make it feel like <i>you</i>.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    with st.form("tiny_form"):
        t = st.session_state.tiny
        t["nickname"] = st.text_input("what do i call you?", value=t["nickname"], placeholder="e.g., baby / dipika / my favorite person")
        t["snack"] = st.text_input("comfort snack?", value=t["snack"], placeholder="e.g., chocolate / chips / ice cream")
        t["color"] = st.selectbox("pick a color that feels like you", ["", "pink", "white", "black", "blue", "purple", "red", "other"], index=0)
        t["mood"] = st.selectbox("today’s mood", ["", "soft", "cute", "chaotic", "sleepy", "romantic", "main character"], index=0)
        st.markdown('<div class="bigBtn">', unsafe_allow_html=True)
        saved = st.form_submit_button("save & continue")
        st.markdown("</div>", unsafe_allow_html=True)
    if saved:
        go(2)
    card_close()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("back"):
            go(0)
    with c2:
        if st.button("continue"):
            go(2)

def page_quiz() -> None:
    card_open()
    st.markdown("<div class='h1'>quick vibe check</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>not science. just me collecting evidence that we’re cute together.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    q = st.session_state.quiz
    if not q["done"]:
        with st.form("quiz"):
            a1 = st.selectbox("ideal date energy", ["cozy café", "movie night", "walk + photos", "fancy dinner"])
            a2 = st.selectbox("gift energy", ["handwritten note", "chocolate", "flowers", "a surprise plan"])
            a3 = st.selectbox("music energy", ["soft + calm", "pop", "bollywood", "anything if it’s together"])
            a4 = st.selectbox("pet energy", ["cat energy", "golden retriever energy", "both", "sleepy panda"])
            st.markdown('<div class="bigBtn">', unsafe_allow_html=True)
            ok = st.form_submit_button("calculate (dramatically)")
            st.markdown("</div>", unsafe_allow_html=True)
        if ok:
            score = 78
            if a1 in ["cozy café", "movie night"]:
                score += 8
            if a2 in ["handwritten note", "a surprise plan"]:
                score += 8
            if a3 == "anything if it’s together":
                score += 8
            if a4 == "cat energy":
                score += 8
            q["done"] = True
            q["score"] = min(score, 100)
            q["answers"] = {"date": a1, "gift": a2, "music": a3, "pet": a4}
            st.experimental_rerun()
    else:
        st.markdown(f"""
        <div class="kgrid">
          <div class="k"><div class="t">compatibility</div><div class="v">{q['score']}%</div></div>
          <div class="k"><div class="t">diagnosis</div><div class="v">down bad</div></div>
          <div class="k"><div class="t">recommended</div><div class="v">say yes</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        if st.button("recalculate (if you’re indecisive)"):
            q["done"] = False
            q["score"] = 0
            q["answers"] = {}
            st.experimental_rerun()
    card_close()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("back"):
            go(1)
    with c2:
        if st.button("continue"):
            go(3)

def page_plan() -> None:
    card_open()
    st.markdown("<div class='h1'>pick the plan</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>you choose. i execute. that’s the deal.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.session_state.plan = st.multiselect(
        "what are we doing?",
        ["café + dessert", "flowers", "movie night", "walk + photos", "surprise itinerary", "stay in + cozy night", "fancy dinner"],
        default=st.session_state.plan
    )
    chosen = ", ".join(st.session_state.plan) if st.session_state.plan else "something we decide together"
    st.markdown(f"<p class='sub'><b>current plan:</b> {chosen}</p>", unsafe_allow_html=True)
    card_close()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("back"):
            go(2)
    with c2:
        if st.button("continue"):
            go(4)

def page_memory() -> None:
    card_open()
    st.markdown("<div class='h1'>memory lane</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>write like you’re texting me. messy is fine. cute is perfect.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    mem = st.session_state.mem
    with st.form("mem"):
        mem["first"] = st.text_area("first impression", value=mem["first"], height=80, placeholder="e.g., i felt calm around you instantly")
        mem["moment"] = st.text_area("favorite moment", value=mem["moment"], height=80, placeholder="e.g., that time we laughed for no reason")
        mem["love"] = st.text_area("one thing i love about you", value=mem["love"], height=80, placeholder="e.g., how you care, even when you pretend you don’t")
        st.markdown('<div class="bigBtn">', unsafe_allow_html=True)
        ok = st.form_submit_button("save & show me the letter")
        st.markdown("</div>", unsafe_allow_html=True)
    if ok:
        mem["saved"] = True
        st.experimental_rerun()
    if mem.get("saved"):
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("<p class='sub'><b>preview</b></p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='card' style='background:rgba(255,255,255,0.90)'><div class='pad' style='padding:18px;'>"
            f"<pre style='white-space:pre-wrap; font-family: ui-sans-serif, system-ui; margin:0;'>"
            f"{build_letter()}" +
            "</pre></div></div>",
            unsafe_allow_html=True
        )
    card_close()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("back"):
            go(3)
    with c2:
        if st.button("continue"):
            go(5)

def page_final() -> None:
    card_open()
    st.markdown(f"<div class='h1'>{GF_NAME}, last screen.</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>okay jokes aside… i’m asking properly now.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    card_close()
    st.markdown("<h1 style='margin-top:12px; font-size:54px; letter-spacing:-1.4px;'>Will you be my Valentine?</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>the “no” button will try. it will fail.</p>", unsafe_allow_html=True)
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.markdown('<div class="bigBtn">', unsafe_allow_html=True)
        if st.button("yes, i will 💗"):
            st.session_state.yes = True
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.components.v1.html("""
        <div style="height:140px;border-radius:20px;border:1px solid rgba(36,26,34,0.10);
        background:rgba(255,255,255,0.92);box-shadow:0 18px 46px rgba(255,47,146,0.12);
        position:relative;overflow:hidden;padding:14px;">
          <div style="font-weight:900;color:rgba(36,26,34,0.86);margin-bottom:10px;">No (if you can)</div>
          <button id="noBtn" style="position:absolute;left:18%;top:66px;height:46px;padding:0 14px;border-radius:16px;
            border:1px solid rgba(255,47,146,0.22);background:rgba(255,47,146,0.08);font-weight:900;font-size:14px;
            color:rgba(36,26,34,0.92);cursor:pointer;transition:transform .12s ease, opacity .18s ease, filter .18s ease;">
            no
          </button>
          <div id="msg" style="position:absolute;left:14px;bottom:10px;font-size:12px;color:rgba(107,92,102,0.95);">
            come closer.
          </div>
        </div>
        <script>
        (function(){
          const btn = document.getElementById("noBtn");
          const msg = document.getElementById("msg");
          let t=0;
          function clamp(n,a,b){return Math.max(a, Math.min(b,n));}
          function rand(min,max){return Math.random()*(max-min)+min;}
          function move(){ btn.style.left = rand(6,72) + "%"; }
          function setMsg(){
            const lines=["no is… loading","nice try","it’s shy","please press yes","option removed"];
            msg.textContent = lines[Math.min(t, lines.length-1)];
          }
          function fade(){
            if(t===1){btn.textContent="nope"; btn.style.transform="scale(0.92)";}
            else if(t===2){btn.textContent="…"; btn.style.transform="scale(0.84) rotate(-2deg)";}
            else if(t===3){btn.style.filter="blur(1.2px)"; btn.style.transform="scale(0.76) rotate(2deg)";}
            else if(t===4){btn.style.opacity="0.45"; btn.style.transform="scale(0.68)"; btn.textContent="";}
            else if(t>=5){btn.style.opacity="0"; btn.style.pointerEvents="none"; msg.textContent="no has left the chat.";}
          }
          const box = btn.parentElement;
          box.addEventListener("mousemove",(e)=>{
            if(btn.style.pointerEvents==="none") return;
            const r=btn.getBoundingClientRect();
            const dx=e.clientX-(r.left+r.width/2);
            const dy=e.clientY-(r.top+r.height/2);
            if(Math.sqrt(dx*dx+dy*dy)<70){
              t=clamp(t+1,0,99);
              move(); setMsg(); fade();
            }
          });
          btn.addEventListener("click",()=>{
            t=clamp(t+2,0,99);
            move(); setMsg(); fade();
          });
          setTimeout(move,200);
        })();
        </script>
        """, height=160)
    if st.session_state.yes:
        st.balloons()
        letter = build_letter()
        try:
            pdf = make_pdf(letter)
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown("<p class='sub'><b>your letter</b></p>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='card' style='background:rgba(255,255,255,0.92)'><div class='pad' style='padding:18px;'>"
                f"<pre style='white-space:pre-wrap; font-family: ui-sans-serif, system-ui; margin:0;'>"
                f"{letter}</pre></div></div>",
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.download_button(
                "download the certificate (pdf)",
                data=pdf,
                file_name="valentine_certificate.pdf",
                mime="application/pdf",
            )
        except RuntimeError as e:
            st.error(str(e))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("replay"):
                for k in ["step","tiny","quiz","plan","mem","yes"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.experimental_rerun()
        with c2:
            if st.button("back to memory lane"):
                st.session_state.yes = False
                go(4)


# ---------------------------------------------------------------------------
# Main entry point

def main() -> None:
    init_state()
    inject_theme()
    if st.session_state.step == 0:
        page_boot()
    elif st.session_state.step == 1:
        page_tiny()
    elif st.session_state.step == 2:
        page_quiz()
    elif st.session_state.step == 3:
        page_plan()
    elif st.session_state.step == 4:
        page_memory()
    else:
        page_final()


if __name__ == "__main__":
    main()