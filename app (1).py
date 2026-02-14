"""
An improved version of the interactive Valentine certificate app.

This script builds upon the original Streamlit application shared by the user.
It maintains the same playful flow of collecting small details, running a
simple compatibility quiz, choosing a date plan, reminiscing about shared
memories and ultimately asking "Will you be my Valentine?"  The
improvements focus on usability and aesthetics:

* A cohesive pookie-inspired pastel colour palette drawn from a "Valentine's
  Day Pookie" palette; these colours were sourced from a palette that
  features blush rose (#f4c2c2) with warm raspberry (#d86f79), golden
  caramel (#c58b55), soft cocoa (#8b5e3b) and creamy vanilla (#faebd7)
  documented on a colour reference site【660647952852864†L41-L54】.
* Floating heart decorations subtly animate across the background without
  overwhelming the content.
* Simplified navigation: each page only shows a single set of back/next
  buttons to avoid confusion.
* Minor bug fixes for state handling and rendering when rerunning a form.
* A matching colour scheme for the generated PDF certificate.

To run the app locally, save this file and execute `streamlit run
valentine_pookie_app.py` from your terminal.  The only dependencies
beyond Streamlit are reportlab (for PDF generation).  Install both via
`pip install streamlit reportlab`.
"""

import random
import time
import textwrap
from io import BytesIO

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# ----- Configuration -----
# Change these values to personalise the letter.  They are deliberately kept
# separate from the rest of the code so it's obvious where to customise.
GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"

# Define a pookie-inspired colour palette.  These colours come from a
# Valentine's Day palette that blends blush rose (#f4c2c2) with warm
# raspberry (#d86f79), golden caramel (#c58b55), soft cocoa (#8b5e3b) and
# creamy vanilla (#faebd7)【660647952852864†L41-L54】.  Throughout the app we
# reference these as CSS variables to ensure consistency between the web UI
# and the generated PDF certificate.
POOKIE_COLORS = {
    "rose": "#f4c2c2",        # blush rose
    "raspberry": "#d86f79",   # warm raspberry
    "caramel": "#c58b55",    # golden caramel
    "cocoa": "#8b5e3b",      # soft cocoa
    "vanilla": "#faebd7"      # creamy vanilla
}

# ----- Streamlit page config -----
st.set_page_config(page_title="Be my Valentine", page_icon="💌", layout="centered")


def inject_styles() -> None:
    """Inject custom CSS into the Streamlit app.

    The theme is intentionally soft and warm.  We use the POOKIE_COLORS to
    define custom CSS variables.  Floating hearts are created with pseudo
    elements and CSS animations rather than external images so there are no
    external dependencies.  The base styles ensure inputs, buttons and cards
    harmonise with the palette.
    """

    css = f"""
    <style>
    /* Hide default Streamlit chrome */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* Colour variables derived from the pookie palette */
    :root {{
      --rose: {POOKIE_COLORS['rose']};
      --raspberry: {POOKIE_COLORS['raspberry']};
      --caramel: {POOKIE_COLORS['caramel']};
      --cocoa: {POOKIE_COLORS['cocoa']};
      --vanilla: {POOKIE_COLORS['vanilla']};
      --shadow: 0 20px 50px rgba(0,0,0,0.08);
    }}

    .stApp {{
      background: linear-gradient(180deg, var(--vanilla) 0%, var(--rose) 50%, var(--vanilla) 100%);
      position: relative;
      overflow: hidden;
    }}

    /* Floating hearts container */
    .heart-container {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      /* place hearts behind the rest of the app */
      pointer-events: none;
      z-index: -1;
    }}
    .heart {{
      position: absolute;
      width: 20px;
      height: 20px;
      background: var(--raspberry);
      transform: rotate(45deg);
      opacity: 0.7;
    }}
    .heart::before,
    .heart::after {{
      content: "";
      position: absolute;
      width: 20px;
      height: 20px;
      background: var(--raspberry);
      border-radius: 50%;
    }}
    .heart::before {{ top: -10px; left: 0; }}
    .heart::after {{ left: -10px; top: 0; }}
    /* Create varying animations */
    @keyframes float {{
      0% {{ transform: translateY(0) scale(1); opacity:0; }}
      10% {{ opacity:0.8; }}
      100% {{ transform: translateY(-120vh) scale(1.6); opacity:0; }}
    }}

    /* Card styling */
    .shell {{ position: relative; z-index: 1; }}
    .card {{
      border-radius: 24px;
      background: rgba(255,255,255,0.95);
      box-shadow: var(--shadow);
      padding: 24px;
    }}
    .h1 {{
      font-size: 42px;
      font-weight: 800;
      color: var(--cocoa);
      margin-bottom: 8px;
    }}
    .sub {{
      font-size: 15px;
      color: var(--cocoa);
      margin-top: 0;
      margin-bottom: 18px;
    }}
    .chipRow {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 12px; }}
    .chip {{
      font-size: 12px;
      padding: 5px 8px;
      border-radius: 12px;
      background: rgba(255,255,255,0.85);
      border: 1px solid var(--caramel);
      color: var(--cocoa);
    }}
    .hr {{ height:1px; background: rgba(0,0,0,0.05); margin: 18px 0; }}

    /* Buttons */
    div.stButton > button {{
      border-radius: 16px !important;
      font-weight: 800 !important;
      background: var(--raspberry) !important;
      color: white !important;
      height: 50px;
      border: none;
      box-shadow: 0 14px 34px rgba(0,0,0,0.12) !important;
    }}
    div.stButton > button:hover {{
      filter: brightness(1.05);
      transform: translateY(-2px);
    }}

    /* Inputs */
    input, textarea, select {{
      border-radius: 14px !important;
      border: 1px solid var(--caramel) !important;
      padding: 8px 12px !important;
      background: rgba(255,255,255,0.98) !important;
      color: var(--cocoa) !important;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # Inject hearts via a custom component.  We use random positions and delays
    # from within Python to generate hearts so they don't all animate in sync.
    hearts_html = [
        f"<div class='heart' style='left:{random.randint(0,95)}%; top:{100 + i*5}%; animation: float {random.randint(8,14)}s infinite {i*1.5}s;'></div>"
        for i in range(10)
    ]
    st.markdown(
        f"<div class='heart-container'>{''.join(hearts_html)}</div>",
        unsafe_allow_html=True
    )


# ----- State management -----
STEPS = ["Boot", "Tiny things", "Little quiz", "Pick a plan", "Memory lane", "Final"]

def init_state():
    st.session_state.setdefault("step", 0)
    st.session_state.setdefault("tiny", {"nickname": "", "snack": "", "color": "", "mood": ""})
    st.session_state.setdefault("quiz", {"done": False, "score": 0, "answers": {}})
    st.session_state.setdefault("plan", [])
    st.session_state.setdefault("mem", {"first": "", "moment": "", "love": "", "saved": False})
    st.session_state.setdefault("yes", False)

def goto_step(i: int):
    st.session_state.step = max(0, min(i, len(STEPS) - 1))
    st.experimental_rerun()

def stepper() -> None:
    """Render a simple progress indicator with hearts."""
    total = len(STEPS)
    current = st.session_state.step + 1
    hearts = [
        f"<span style='color: var(--raspberry); font-size: 20px;'>{'❤' if i < current else '♡'}</span>"
        for i in range(total)
    ]
    st.markdown(
        f"<div style='margin-top:8px;'>{''.join(hearts)} <span style='font-size:12px; color:var(--cocoa); margin-left:6px;'>"
        f"{STEPS[st.session_state.step]} ({current}/{total})</span></div>",
        unsafe_allow_html=True
    )
    st.progress(current/total)


# ----- Letter generator -----
def build_letter() -> str:
    """Create the text for the letter based on collected inputs."""
    t = st.session_state.tiny
    m = st.session_state.mem
    nick = (t["nickname"].strip() or GF_NAME)
    snack = (t["snack"].strip() or "something sweet")
    plan = ", ".join(st.session_state.plan) if st.session_state.plan else "something we decide together"

    first = (m["first"].strip() or "I remember thinking: yep... she’s special.")
    moment = (m["moment"].strip() or "one of those small moments that randomly makes me smile later.")
    love = (m["love"].strip() or "how easy it feels to be myself around you.")

    return (
        f"Hey {nick},\n\n"
        f"I made this because I wanted to do something cute for you - the kind of cute that's a little embarrassing, but in a good way.\n\n"
        f"I still remember my first impression: {first}\n"
        f"My favourite moment: {moment}\n"
        f"And one thing I genuinely love about you: {love}\n\n"
        f"For Valentine's, I'm claiming you for a {plan} kind of day — and yes, there will be {snack}.\n\n"
        f"Okay now... serious question.\n\n"
        f"— {YOUR_NAME}"
    )


# ----- PDF generator -----
def make_pdf(letter_text: str) -> bytes:
    """Generate a PDF certificate using the pookie palette."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    margin = 1.6 * cm

    # Outer border using raspberry colour
    c.setLineWidth(2)
    c.setStrokeColorRGB(216/255.0, 111/255.0, 121/255.0)  # raspberry
    c.roundRect(margin, margin, w - 2*margin, h - 2*margin, 18, stroke=1, fill=0)

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(139/255.0, 94/255.0, 59/255.0)  # cocoa
    c.drawCentredString(w/2, h - 3.0*cm, "Valentine Certificate")

    # Subtitle
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(197/255.0, 139/255.0, 85/255.0)  # caramel
    c.drawCentredString(w/2, h - 3.8*cm, "handmade (by a slightly nervous boyfriend)")

    # Names
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(139/255.0, 94/255.0, 59/255.0)  # cocoa
    c.drawCentredString(w/2, h - 5.2*cm, f"{YOUR_NAME}  ↔  {GF_NAME}")

    # Content box
    box_x = 2.2 * cm
    box_y = 4.0 * cm
    box_w = w - 4.4 * cm
    box_h = h - 10.8 * cm

    c.setLineWidth(1)
    # Use rose as stroke and vanilla as fill
    c.setStrokeColorRGB(244/255.0, 194/255.0, 194/255.0)  # rose
    c.setFillColorRGB(250/255.0, 235/255.0, 215/255.0)    # vanilla
    c.roundRect(box_x, box_y, box_w, box_h, 14, stroke=1, fill=1)

    # Text
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(139/255.0, 94/255.0, 59/255.0)  # cocoa

    # Wrap text manually
    lines = []
    for para in letter_text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur_line = ""
        for w0 in words:
            trial = (cur_line + " " + w0).strip()
            if c.stringWidth(trial, "Helvetica", 11) <= box_w - 1.2 * cm:
                cur_line = trial
            else:
                lines.append(cur_line)
                cur_line = w0
        if cur_line:
            lines.append(cur_line)

    x = box_x + 0.6 * cm
    y = box_y + box_h - 0.9 * cm
    for ln in lines:
        if y < box_y + 0.8 * cm:
            break
        c.drawString(x, y, ln)
        y -= 14

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(197/255.0, 139/255.0, 85/255.0)  # caramel
    c.drawCentredString(w/2, margin + 0.9 * cm, "This document is legally binding in my heart. (And only there.)")

    c.showPage()
    c.save()
    return buf.getvalue()


# ----- Page implementations -----
def page_boot():
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>okay hi.</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='sub'>this is for <b>{GF_NAME}</b>. it's short, cute and slightly unfair to the 'no' button.</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='chipRow'>"
        "<span class='chip'>compiling feelings…</span>"
        "<span class='chip'>linking cuddles…</span>"
        "<span class='chip'>optimising hugs…</span>"
        "</div>",
        unsafe_allow_html=True
    )
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # Simple loading messages as before, but with shorter wait to keep users engaged.
    msgs = [
        "checking if your smile is online... ✅",
        "warming up the cute stuff...",
        "loading tiny butterflies...",
        "setting the 'no' button to hard mode...",
        "almost done. don't blink."
    ]
    spot = st.empty()
    prog = st.progress(0)
    for i in range(100):
        if i % 20 == 0:
            spot.markdown(f"<div class='sub'>{random.choice(msgs)}</div>", unsafe_allow_html=True)
        time.sleep(0.01)
        prog.progress(i + 1)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    if st.button("start"):
        goto_step(1)
    st.markdown("</div></div>", unsafe_allow_html=True)


def page_tiny():
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>tiny things about you</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>nothing deep. just the cute details that make it feel like <i>you</i>.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    t = st.session_state.tiny
    with st.form("tiny_form"):
        t["nickname"] = st.text_input("what do i call you?", value=t["nickname"], placeholder="e.g., baby / dipika / my favourite person")
        t["snack"] = st.text_input("comfort snack?", value=t["snack"], placeholder="e.g., chocolate / chips / ice cream")
        t["color"] = st.selectbox(
            "pick a colour that feels like you",
            ["", "pink", "white", "black", "blue", "purple", "red", "other"],
            index=0
        )
        t["mood"] = st.selectbox(
            "today's mood",
            ["", "soft", "cute", "chaotic", "sleepy", "romantic", "main character"],
            index=0
        )
        if st.form_submit_button("save & continue"):
            goto_step(2)

    st.markdown("</div></div>", unsafe_allow_html=True)
    # navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(0)
    with c2:
        if st.button("continue →"):
            goto_step(2)


def page_quiz():
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
                # Simple scoring as in the original script
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
                st.experimental_rerun()
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
            unsafe_allow_html=True
        )
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        if st.button("recalculate (if you're indecisive)"):
            q["done"] = False
            q["score"] = 0
            q["answers"] = {}
            st.experimental_rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    # navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← back"):
            goto_step(1)
    with c2:
        if st.button("continue →"):
            goto_step(3)


def page_plan():
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
            "fancy dinner"
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
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='h1'>memory lane</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>write like you're texting me. messy is fine. cute is perfect.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    mem = st.session_state.mem
    with st.form("mem_form"):
        mem["first"] = st.text_area("first impression", value=mem["first"], height=80, placeholder="e.g., i felt calm around you instantly")
        mem["moment"] = st.text_area("favourite moment", value=mem["moment"], height=80, placeholder="e.g., that time we laughed for no reason")
        mem["love"] = st.text_area("one thing i love about you", value=mem["love"], height=80, placeholder="e.g., how you care, even when you pretend you don't")
        if st.form_submit_button("save & show me the letter"):
            mem["saved"] = True
            st.experimental_rerun()

    if mem["saved"]:
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("<p class='sub'><b>preview</b></p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='card' style='background:rgba(255,255,255,0.92);'><pre style='white-space:pre-wrap; margin:0;'>"
            f"{build_letter()}</pre></div>",
            unsafe_allow_html=True
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
    st.markdown("<div class='shell'><div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='h1'>{GF_NAME}, last screen.</div>", unsafe_allow_html=True)
    st.markdown("<p class='sub'>okay jokes aside… i'm asking properly now.</p>", unsafe_allow_html=True)
    stepper()
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Display the main question heading.  Use a single string literal so there are no
    # stray empty strings that could confuse the rendering engine.
    st.markdown(
        "<h1 style='margin-top:12px; font-size:54px; font-weight:800; "
        "color:var(--cocoa); letter-spacing:-1.4px;'>Will you be my Valentine?</h1>",
        unsafe_allow_html=True
    )
    st.markdown("<p class='sub'>the 'no' button will try. it will fail.</p>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        if st.button("yes, i will 💗"):
            st.session_state.yes = True
            st.experimental_rerun()
    with right:
        st.components.v1.html(
            """
<div style="height:140px;border-radius:20px;border:1px solid var(--caramel);
background:rgba(255,255,255,0.92);box-shadow:0 18px 46px rgba(0,0,0,0.10);
position:relative;overflow:hidden;padding:14px;">
  <div style="font-weight:900;color:var(--cocoa);margin-bottom:10px;">No (if you can)</div>
  <button id="noBtn" style="position:absolute;left:18%;top:66px;height:46px;padding:0 14px;border-radius:16px;
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
  const btn = document.getElementById("noBtn");
  const msg = document.getElementById("msg");
  let t=0;
  function clamp(n,a,b){return Math.max(a, Math.min(b,n));}
  function rand(min,max){return Math.random()*(max-min)+min;}
  function move(){ btn.style.left = rand(5,75) + "%"; }
  function setMsg(){
    const lines=["no is… loading","nice try","it's shy","please press yes","option removed"];
    msg.textContent = lines[Math.min(t, lines.length-1)];
  }
  function fade(){
    if(t===1){btn.textContent="nope"; btn.style.transform="scale(0.92)";}
    else if(t===2){btn.textContent="…"; btn.style.transform="scale(0.86) rotate(-2deg)";}
    else if(t===3){btn.style.filter="blur(1.2px)"; btn.style.transform="scale(0.78) rotate(2deg)";}
    else if(t===4){btn.style.opacity="0.45"; btn.style.transform="scale(0.70)"; btn.textContent="";}
    else if(t>=5){btn.style.opacity="0"; btn.style.pointerEvents="none"; msg.textContent="no has left the chat.";}
  }
  const box = btn.parentElement;
  box.addEventListener("mousemove",(e)=>{
    if(btn.style.pointerEvents === "none") return;
    const r = btn.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width/2);
    const dy = e.clientY - (r.top + r.height/2);
    if(Math.sqrt(dx*dx + dy*dy) < 60){
      t = clamp(t+1,0,99);
      move(); setMsg(); fade();
    }
  });
  btn.addEventListener("click",()=>{
    t = clamp(t+2,0,99);
    move(); setMsg(); fade();
  });
  setTimeout(move,200);
})();
</script>
""",
            height=160,
        )

    if st.session_state.yes:
        st.balloons()
        letter = build_letter()
        pdf = make_pdf(letter)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<p class='sub'><b>your letter</b></p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='card' style='background:rgba(255,255,255,0.92);'><pre style='white-space:pre-wrap; margin:0;'>"
            f"{letter}</pre></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.download_button(
            "download the certificate (pdf)",
            data=pdf,
            file_name="valentine_certificate.pdf",
            mime="application/pdf",
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("replay"):
                for k in ["step", "tiny", "quiz", "plan", "mem", "yes"]:
                    st.session_state.pop(k, None)
                st.experimental_rerun()
        with c2:
            if st.button("back to memory lane"):
                st.session_state.yes = False
                goto_step(4)


def main():
    init_state()
    inject_styles()
    step = st.session_state.step
    if step == 0:
        page_boot()
    elif step == 1:
        page_tiny()
    elif step == 2:
        page_quiz()
    elif step == 3:
        page_plan()
    elif step == 4:
        page_memory()
    else:
        page_final()


if __name__ == "__main__":
    main()