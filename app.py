"""
Valentine Certificate Streamlit App with Floating Hearts

This Streamlit application provides a playful, interactive way to ask
someone to be your Valentine.  It guides the recipient through a
series of mini‐pages: a boot screen, some light‐hearted questions
about themselves, a compatibility quiz, a selection of date plans and
a memory lane where you can write down shared moments.  At the end
there's the big question with a mischievous “no” button that tries
to avoid being clicked.  If your partner accepts, the app generates a
PDF certificate with a personalised letter, which can be downloaded.

The floating hearts are implemented purely in CSS.  They float
upwards behind the content without interfering with any interactive
elements.  The colours are inspired by a pookie‑themed Valentine
palette featuring blush rose, warm raspberry, golden caramel, soft
cocoa and creamy vanilla【660647952852864†L41-L54】.

To run the app, install the dependencies with `pip install
streamlit reportlab` and then execute `streamlit run app.py`.
"""

from __future__ import annotations

import time
from io import BytesIO
from typing import Dict, List

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Configure the Streamlit page before any other Streamlit calls.  This must
# happen prior to injecting CSS or using other st.* functions.  See
# https://discuss.streamlit.io/t/setting-page-config/ for details.
st.set_page_config(page_title="💗 Valentine", page_icon="💗", layout="centered")


# ---------------------------------------------------------------------------
# Configuration

# Names of the couple.  Feel free to personalise these constants.
GF_NAME: str = "Dipika"
YOUR_NAME: str = "Tanmay"

# A pookie‑inspired colour palette: blush rose, warm raspberry,
# golden caramel, soft cocoa and creamy vanilla【660647952852864†L41-L54】.
PALETTE: Dict[str, str] = {
    "rose": "#f4c2c2",
    "raspberry": "#d86f79",
    "caramel": "#c58b55",
    "cocoa": "#8b5e3b",
    "vanilla": "#faebd7",
}


# ---------------------------------------------------------------------------
# CSS and floating hearts
def inject_css() -> None:
    """Inject custom styles and a floating hearts overlay.

    The hearts are absolutely positioned within a fixed container
    covering the viewport.  Each heart uses CSS keyframes to float
    upwards.  The container has `pointer-events: none` so clicks and
    hovers pass through to the Streamlit widgets beneath.
    """
    css = f"""
    <style>
    /* Hide Streamlit's default header and footer */
    #MainMenu, header, footer {{display: none;}}

    /* Use CSS variables for our palette */
    :root {{
      --rose: {PALETTE['rose']};
      --raspberry: {PALETTE['raspberry']};
      --caramel: {PALETTE['caramel']};
      --cocoa: {PALETTE['cocoa']};
      --vanilla: {PALETTE['vanilla']};
    }}

    /* Overall page background */
    .stApp {{
      background: linear-gradient(180deg, var(--vanilla) 0%, var(--rose) 50%, var(--vanilla) 100%);
      position: relative;
      z-index: 1;
    }}

    /* Cards and typography */
    .shell {{ position: relative; z-index: 2; }}
    .card {{
      background: rgba(255, 255, 255, 0.95);
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 14px 40px rgba(0, 0, 0, 0.12);
    }}
    .h1 {{ font-size: 42px; font-weight: 800; color: var(--cocoa); margin-bottom: 6px; }}
    .sub {{ font-size: 15px; color: var(--cocoa); margin: 0 0 18px 0; }}
    .hr {{ height: 1px; background: rgba(0,0,0,0.08); margin: 18px 0; }}
    .chipRow {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
    .chip {{
      font-size: 12px;
      padding: 5px 8px;
      border-radius: 12px;
      background: rgba(255,255,255,0.85);
      border: 1px solid var(--caramel);
      color: var(--cocoa);
    }}

    /* Input controls */
    input, textarea, select {{
      border-radius: 14px !important;
      border: 1px solid var(--caramel) !important;
      padding: 8px 12px !important;
      background: rgba(255,255,255,0.98) !important;
      color: var(--cocoa) !important;
    }}

    /* Buttons */
    div.stButton > button {{
      border-radius: 14px !important;
      font-weight: 700 !important;
      height: 48px;
      border: none;
      background: var(--raspberry) !important;
      color: white !important;
      box-shadow: 0 10px 30px rgba(0,0,0,0.10) !important;
    }}
    div.stButton > button:hover {{ filter: brightness(1.05); transform: translateY(-2px); }}

    /* Floating hearts container */
    .heart-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
      overflow: hidden;
    }}
    .heart {{
      position: absolute;
      bottom: -40px;
      width: 20px;
      height: 20px;
      background: var(--raspberry);
      transform: rotate(45deg);
      opacity: 0.8;
      animation: floatUp var(--duration) linear infinite;
      animation-delay: var(--delay);
    }}
    .heart::before,
    .heart::after {{
      content: "";
      position: absolute;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--raspberry);
    }}
    .heart::before {{ top: -10px; left: 0; }}
    .heart::after  {{ left: -10px; top: 0; }}
    @keyframes floatUp {{
      0% {{ transform: translateY(0) rotate(45deg) scale(1); opacity: 0; }}
      10% {{ opacity: 0.9; }}
      100% {{ transform: translateY(-120vh) rotate(45deg) scale(1.6); opacity: 0; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Generate hearts markup.  Each heart has its own left position,
    # animation duration and delay defined via CSS variables.
    positions: List[int] = [5, 15, 25, 35, 45, 55, 65, 75, 85, 20, 40, 60, 80]
    durations: List[int] = [14, 16, 18, 20, 15, 17, 19, 13, 21, 22, 18, 16, 20]
    delays: List[float] = [0.0, 2.0, 3.5, 1.5, 4.0, 2.5, 1.0, 5.0, 3.0, 0.5, 1.2, 2.8, 4.5]
    hearts_html = "<div class='heart-overlay'>"
    for pos, dur, dly in zip(positions, durations, delays):
        hearts_html += (
            f"<div class='heart' style='left:{pos}%; --duration:{dur}s; --delay:{dly}s;'></div>"
        )
    hearts_html += "</div>"
    st.markdown(hearts_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# State management

STEPS: List[str] = [
    "Boot",
    "Tiny things",
    "Little quiz",
    "Pick a plan",
    "Memory lane",
    "Final",
]


def init_state() -> None:
    """Initialise session state on first run."""
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("tiny", {"nickname": "", "snack": "", "color": "", "mood": ""})
    st.session_state.setdefault("quiz", {"done": False, "score": 0, "answers": {}})
    st.session_state.setdefault("plan", [])
    st.session_state.setdefault("mem", {"first": "", "moment": "", "love": "", "saved": False})
    st.session_state.setdefault("yes", False)


def goto_step(target: int) -> None:
    """Navigate to a specific step and rerun the app."""
    st.session_state.step = max(0, min(target, len(STEPS) - 1))
    st.rerun()


def stepper() -> None:
    """Render a simple progress indicator using hearts icons and progress bar."""
    current = st.session_state.step + 1
    total = len(STEPS)
    icons = []
    for i in range(total):
        icon = "❤" if i < current else "♡"
        icons.append(icon)
    # Build the progress indicator HTML.  The span is closed outside
    # of the f-strings to avoid unterminated string errors.
    html = (
        f"<div style='margin-top:8px;'>{''.join(icons)} "
        f"<span style='font-size:12px; color:var(--cocoa); margin-left:6px;'>"
        f"{STEPS[st.session_state.step]} ({current}/{total})"
        "</span></div>"
    )
    st.markdown(html, unsafe_allow_html=True)
    st.progress(current / total)


# ---------------------------------------------------------------------------
# Letter and PDF generation

def build_letter() -> str:
    """Construct the personalised letter from state."""
    tiny = st.session_state.tiny
    mem = st.session_state.mem
    nickname = tiny.get("nickname", "").strip() or GF_NAME
    snack = tiny.get("snack", "").strip() or "something sweet"
    plan_list = st.session_state.plan
    plan_text = ", ".join(plan_list) if plan_list else "something we decide together"
    first = mem.get("first", "").strip() or "I remember thinking: yep... she's special."
    moment = mem.get("moment", "").strip() or "one of those small moments that randomly makes me smile later."
    love = mem.get("love", "").strip() or "how easy it feels to be myself around you."
    return (
        f"Hey {nickname},\n\n"
        f"I made this because I wanted to do something cute for you – the kind of cute that's a little embarrassing, but in a good way.\n\n"
        f"I still remember my first impression: {first}\n"
        f"My favourite moment: {moment}\n"
        f"And one thing I genuinely love about you: {love}\n\n"
        f"For Valentine's, I'm claiming you for a {plan_text} kind of day – and yes, there will be {snack}.\n\n"
        f"Okay now... serious question.\n\n"
        f"— {YOUR_NAME}"
    )


def make_pdf(letter_text: str) -> bytes:
    """Generate a PDF certificate from the letter text using reportlab."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    margin = 1.6 * cm
    # Outer border
    c.setLineWidth(2)
    # Raspberry colour border
    c.setStrokeColorRGB(216 / 255.0, 111 / 255.0, 121 / 255.0)
    c.roundRect(margin, margin, w - 2 * margin, h - 2 * margin, 18, stroke=1, fill=0)
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(139 / 255.0, 94 / 255.0, 59 / 255.0)  # cocoa
    c.drawCentredString(w / 2, h - 3.0 * cm, "Valentine Certificate")
    # Subtitle
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(197 / 255.0, 139 / 255.0, 85 / 255.0)  # caramel
    c.drawCentredString(w / 2, h - 3.8 * cm, "handmade (by a slightly nervous boyfriend)")
    # Names line
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(139 / 255.0, 94 / 255.0, 59 / 255.0)  # cocoa
    c.drawCentredString(w / 2, h - 5.2 * cm, f"{YOUR_NAME}  ↔  {GF_NAME}")
    # Text box
    box_x = 2.2 * cm
    box_y = 4.0 * cm
    box_w = w - 4.4 * cm
    box_h = h - 10.8 * cm
    c.setLineWidth(1)
    # Box background colours (rose border, vanilla fill)
    c.setStrokeColorRGB(244 / 255.0, 194 / 255.0, 194 / 255.0)
    c.setFillColorRGB(250 / 255.0, 235 / 255.0, 215 / 255.0)
    c.roundRect(box_x, box_y, box_w, box_h, 14, stroke=1, fill=1)
    # Write the letter with wrapping
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(139 / 255.0, 94 / 255.0, 59 / 255.0)  # cocoa
    lines: List[str] = []
    for paragraph in letter_text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        current_line = ""
        for word in words:
            trial = (current_line + " " + word).strip()
            if c.stringWidth(trial, "Helvetica", 11) <= box_w - 1.2 * cm:
                current_line = trial
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    x = box_x + 0.6 * cm
    y = box_y + box_h - 0.9 * cm
    for ln in lines:
        if y < box_y + 0.8 * cm:
            break
        c.drawString(x, y, ln)
        y -= 14
    # Footer note
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(197 / 255.0, 139 / 255.0, 85 / 255.0)  # caramel
    c.drawCentredString(w / 2, margin + 0.9 * cm, "This document is legally binding in my heart. (And only there.)")
    c.showPage()
    c.save()
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Page definitions

def page_boot():
    """Render the boot screen with a playful loading sequence."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>okay hi.</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='sub'>this is for <b>{GF_NAME}</b>. it's short, cute and slightly unfair to the 'no' button.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='chipRow'>"
        "<span class='chip'>compiling feelings...</span>"
        "<span class='chip'>linking cuddles...</span>"
        "<span class='chip'>optimising hugs...</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    # Simulated loading messages
    messages = [
        "checking if your smile is online... ✅",
        "warming up the cute stuff...",
        "loading tiny butterflies...",
        "setting the 'no' button to hard mode...",
        "almost done. don't blink."
    ]
    spot = st.empty()
    prog = st.progress(0)
    for i in range(80):
        if i % 16 == 0:
            spot.markdown(f"<div class='sub'>{messages[(i // 16) % len(messages)]}</div>", unsafe_allow_html=True)
        time.sleep(0.01)
        prog.progress(i + 1)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    if st.button("start"):
        goto_step(1)
    st.markdown("</div></div>", unsafe_allow_html=True)


def page_tiny():
    """Collect tiny details about the recipient."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>tiny things about you</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='sub'>nothing deep. just the cute details that make it feel like <i>you</i>.</p>",
        unsafe_allow_html=True,
    )
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    tiny = st.session_state.tiny
    with st.form("tiny_form"):
        tiny["nickname"] = st.text_input("what do i call you?", value=tiny["nickname"], placeholder="e.g., baby / dipika / my favourite person")
        tiny["snack"] = st.text_input("comfort snack?", value=tiny["snack"], placeholder="e.g., chocolate / chips / ice cream")
        tiny["color"] = st.selectbox("pick a colour that feels like you", ["", "pink", "white", "black", "blue", "purple", "red", "other"], index=0)
        tiny["mood"] = st.selectbox("today's mood", ["", "soft", "cute", "chaotic", "sleepy", "romantic", "main character"], index=0)
        if st.form_submit_button("save & continue"):
            goto_step(2)
    st.markdown("</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(0)
    with c2:
        if st.button("continue →"):
            goto_step(2)


def page_quiz():
    """Run a whimsical compatibility quiz."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>quick vibe check</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>not science. just me collecting evidence that we're cute together.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    q = st.session_state.quiz
    if not q["done"]:
        with st.form("quiz_form"):
            a1 = st.selectbox("ideal date energy", ["cozy café", "movie night", "walk + photos", "fancy dinner"])
            a2 = st.selectbox("gift energy", ["handwritten note", "chocolate", "flowers", "a surprise plan"])
            a3 = st.selectbox("music energy", ["soft + calm", "pop", "bollywood", "anything if it's together"])
            a4 = st.selectbox("pet energy", ["cat energy", "golden retriever energy", "both", "sleepy panda"])
            if st.form_submit_button("calculate (dramatically)"):
                score = 78
                if a1 in ["cozy café", "movie night"]:
                    score += 8
                if a2 in ["handwritten note", "a surprise plan"]:
                    score += 8
                if a3 == "anything if it's together":
                    score += 8
                if a4 == "cat energy":
                    score += 8
                q["done"] = True
                q["score"] = min(score, 100)
                q["answers"] = {"date": a1, "gift": a2, "music": a3, "pet": a4}
                st.rerun()
    else:
        st.markdown(
            f"""
            <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:12px;'>
              <div class='card' style='padding:12px; text-align:center;'>
                <div style='font-size:12px; color:var(--cocoa);'>compatibility</div>
                <div style='font-size:18px; font-weight:900; color:var(--raspberry);'>{q["score"]}%</div>
              </div>
              <div class='card' style='padding:12px; text-align:center;'>
                <div style='font-size:12px; color:var(--cocoa);'>diagnosis</div>
                <div style='font-size:18px; font-weight:900; color:var(--raspberry);'>down bad</div>
              </div>
              <div class='card' style='padding:12px; text-align:center;'>
                <div style='font-size:12px; color:var(--cocoa);'>recommended</div>
                <div style='font-size:18px; font-weight:900; color:var(--raspberry);'>say yes</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        if st.button("recalculate (if you're indecisive)"):
            q["done"] = False
            q["score"] = 0
            q["answers"] = {}
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(1)
    with c2:
        if st.button("continue →"):
            goto_step(3)


def page_plan():
    """Let the recipient choose the date plan."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>pick the plan</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>you choose. i execute. that's the deal.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.session_state.plan = st.multiselect(
        "what are we doing?",
        [
            "café + dessert",
            "flowers",
            "movie night",
            "walk + photos",
            "surprise itinerary",
            "stay in + cozy night",
            "fancy dinner",
        ],
        default=st.session_state.plan,
    )
    chosen = ", ".join(st.session_state.plan) if st.session_state.plan else "something we decide together"
    st.markdown(f"<p class='sub'><b>current plan:</b> {chosen}</p>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(2)
    with c2:
        if st.button("continue →"):
            goto_step(4)


def page_memory():
    """Collect memories and display a preview of the letter."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>memory lane</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='sub'>write like you're texting me. messy is fine. cute is perfect.</p>",
        unsafe_allow_html=True,
    )
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    mem = st.session_state.mem
    with st.form("memory_form"):
        mem["first"] = st.text_area("first impression", value=mem["first"], height=80, placeholder="e.g., i felt calm around you instantly")
        mem["moment"] = st.text_area("favourite moment", value=mem["moment"], height=80, placeholder="e.g., that time we laughed for no reason")
        mem["love"] = st.text_area("one thing i love about you", value=mem["love"], height=80, placeholder="e.g., how you care, even when you pretend you don't")
        if st.form_submit_button("save & show me the letter"):
            mem["saved"] = True
            st.rerun()
    if mem.get("saved", False):
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("<p class='sub'><b>preview</b></p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='card' style='background:rgba(255,255,255,0.92);'><pre style='white-space:pre-wrap; margin:0;'>"
            f"{build_letter()}"
            "</pre></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(3)
    with c2:
        if st.button("continue →"):
            goto_step(5)


def page_final():
    """Display the final question and handle the answer."""
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='h1'>{GF_NAME}, last screen.</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>okay jokes aside... i'm asking properly now.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    # Main question
    st.markdown(
        "<h1 style='margin-top:12px; font-size:54px; font-weight:800; color:var(--cocoa); letter-spacing:-1.4px;'>Will you be my Valentine?</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("<p class='sub'>the 'no' button will try. it will fail.</p>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        if st.button("yes, i will 💗"):
            st.session_state.yes = True
            st.rerun()
    with right:
        # Playful 'no' button that evades the cursor.  Use a plain string
        # for the HTML/JS to avoid f-string interpolation issues with braces.
        no_html = """
<div style="height:140px;border-radius:20px;border:1px solid var(--caramel);
background:rgba(255,255,255,0.92);box-shadow:0 18px 46px rgba(0,0,0,0.10);
position:relative;overflow:hidden;padding:14px;">
  <div style="font-weight:900;color:var(--cocoa);margin-bottom:10px;">No (if you can)</div>
  <button id="noBtn" style="position:absolute;left:20%;top:66px;height:46px;padding:0 14px;border-radius:16px;
    border:1px solid var(--raspberry);background:rgba(216,111,121,0.1);font-weight:900;font-size:14px;
    color:var(--cocoa);cursor:pointer;transition:transform .12s ease, opacity .18s ease, filter .18s ease;">
    no
  </button>
  <div id="msg" style="position:absolute;left:14px;bottom:10px;font-size:12px;color:var(--cocoa);">
    come closer.
  </div>
</div>
<script>
(function(){
  const btn = document.getElementById('noBtn');
  const msg = document.getElementById('msg');
  let t = 0;
  function clamp(n,a,b){ return Math.max(a, Math.min(b,n)); }
  function rand(min,max){ return Math.random()*(max-min)+min; }
  function move(){ btn.style.left = rand(5,75) + '%'; }
  function setMsg(){
    const lines = ['no is... loading','nice try','it\'s shy','please press yes','option removed'];
    msg.textContent = lines[Math.min(t, lines.length-1)];
  }
  function fade(){
    if(t === 1){ btn.textContent = 'nope'; btn.style.transform = 'scale(0.92)'; }
    else if(t === 2){ btn.textContent = '...'; btn.style.transform = 'scale(0.86) rotate(-2deg)'; }
    else if(t === 3){ btn.style.filter = 'blur(1.2px)'; btn.style.transform = 'scale(0.78) rotate(2deg)'; }
    else if(t === 4){ btn.style.opacity = '0.45'; btn.style.transform = 'scale(0.70)'; btn.textContent = ''; }
    else if(t >= 5){ btn.style.opacity = '0'; btn.style.pointerEvents = 'none'; msg.textContent = 'no has left the chat.'; }
  }
  const box = btn.parentElement;
  box.addEventListener('mousemove', function(e){
    if(btn.style.pointerEvents === 'none') return;
    const r = btn.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width/2);
    const dy = e.clientY - (r.top + r.height/2);
    if(Math.sqrt(dx*dx + dy*dy) < 60){
      t = clamp(t+1, 0, 99);
      move(); setMsg(); fade();
    }
  });
  btn.addEventListener('click', function(){
    t = clamp(t+2, 0, 99);
    move(); setMsg(); fade();
  });
  setTimeout(move,200);
})();
</script>
        """
        st.components.v1.html(no_html, height=160)
    # If accepted, show the letter and PDF download
    if st.session_state.yes:
        st.balloons()
        letter = build_letter()
        pdf_data = make_pdf(letter)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<p class='sub'><b>your letter</b></p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='card' style='background:rgba(255,255,255,0.92);'><pre style='white-space:pre-wrap; margin:0;'>{letter}</pre></div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.download_button(
            label="download the certificate (pdf)",
            data=pdf_data,
            file_name="valentine_certificate.pdf",
            mime="application/pdf",
        )
        # Replay or back options
        c1, c2 = st.columns(2)
        with c1:
            if st.button("replay"):
                for key in ["step", "tiny", "quiz", "plan", "mem", "yes"]:
                    st.session_state.pop(key, None)
                st.rerun()
        with c2:
            if st.button("back to memory lane"):
                st.session_state.yes = False
                goto_step(4)


# ---------------------------------------------------------------------------
# Main entry point

def main() -> None:
    """Entry point for the app."""
    # initialise state (page config was already set at import time)
    init_state()
    inject_css()
    page_idx = st.session_state.step
    if page_idx == 0:
        page_boot()
    elif page_idx == 1:
        page_tiny()
    elif page_idx == 2:
        page_quiz()
    elif page_idx == 3:
        page_plan()
    elif page_idx == 4:
        page_memory()
    else:
        page_final()


if __name__ == "__main__":
    main()