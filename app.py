import time
import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="A little question 💌",
    page_icon="💗",
    layout="centered",
)

# ----------------------------
# Pinterest-style aesthetic CSS
# ----------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

      :root{
        --bg1: #fff7fb;
        --bg2: #ffeef6;
        --bg3: #f6fbff;
        --ink: rgba(25, 20, 30, 0.92);
        --muted: rgba(25, 20, 30, 0.60);
        --card: rgba(255,255,255,0.72);
        --stroke: rgba(255, 105, 180, 0.22);
        --shadow: 0 20px 70px rgba(255, 105, 180, 0.12);
        --shadow2: 0 12px 40px rgba(60, 120, 255, 0.08);
      }

      .stApp{
        background:
          radial-gradient(1200px 700px at 15% 10%, rgba(255, 192, 203, 0.55) 0%, rgba(255,255,255,0.0) 60%),
          radial-gradient(900px 600px at 80% 20%, rgba(173, 216, 230, 0.40) 0%, rgba(255,255,255,0.0) 60%),
          radial-gradient(800px 600px at 50% 90%, rgba(255, 235, 59, 0.12) 0%, rgba(255,255,255,0.0) 65%),
          linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 45%, var(--bg3) 100%);
      }

      .block-container{
        max-width: 860px;
        padding-top: 2.2rem;
        padding-bottom: 3.2rem;
      }

      /* Hide Streamlit default chrome a bit */
      header, footer { visibility: hidden; }

      /* Typography */
      h1, h2, h3, h4, h5, h6 { font-family: "Fraunces", serif !important; color: var(--ink); }
      p, li, div, span { font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Arial !important; color: var(--ink); }

      /* Primary hero */
      .hero {
        text-align: center;
        margin: 0.4rem 0 1.2rem 0;
      }
      .hero-title{
        font-family: "Fraunces", serif;
        font-size: 2.55rem;
        line-height: 1.05;
        margin: 0.3rem 0 0.4rem 0;
        letter-spacing: -0.6px;
      }
      .hero-sub{
        font-size: 1.05rem;
        color: var(--muted);
        margin: 0 0 0.25rem 0;
      }

      /* Card + glass */
      .glass{
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 22px;
        padding: 1.25rem 1.25rem;
        box-shadow: var(--shadow), var(--shadow2);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
      }

      /* Badge pill */
      .pill{
        display:inline-block;
        padding: 0.32rem 0.72rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 105, 180, 0.18);
        background: rgba(255, 182, 193, 0.22);
        color: rgba(25, 20, 30, 0.78);
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
      }

      /* Shimmer loading bar container */
      .shimmer {
        height: 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(255, 105, 180, 0.18);
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(255, 105, 180, 0.08);
      }
      .shimmer::before{
        content:"";
        display:block;
        height:100%;
        width:40%;
        background: linear-gradient(90deg, rgba(255,105,180,0.0), rgba(255,105,180,0.22), rgba(173,216,230,0.18), rgba(255,105,180,0.0));
        animation: shine 1.25s infinite;
      }
      @keyframes shine {
        0% { transform: translateX(-60%); }
        100% { transform: translateX(260%); }
      }

      /* Streamlit buttons: soften */
      div.stButton > button {
        width: 100%;
        border-radius: 18px;
        padding: 0.9rem 1rem;
        font-size: 1.03rem;
        font-weight: 700;
        border: 1px solid rgba(255, 105, 180, 0.22);
        background: linear-gradient(135deg, rgba(255,105,180,0.18), rgba(173,216,230,0.14), rgba(255,255,255,0.45));
        box-shadow: 0 12px 30px rgba(255, 105, 180, 0.10);
      }
      div.stButton > button:hover {
        transform: translateY(-1px);
        border: 1px solid rgba(255, 105, 180, 0.34);
      }

      /* Letter */
      .letter{
        line-height: 1.7;
        font-size: 1.05rem;
      }
      .signature{
        margin-top: 1rem;
        font-weight: 700;
      }
      .tiny {
        color: var(--muted);
        font-size: 0.95rem;
        text-align: center;
        margin-top: 0.8rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Query param helper (works across Streamlit versions)
# ----------------------------
def get_answer_param() -> str | None:
    # Newer Streamlit
    try:
        qp = st.query_params
        val = qp.get("answer")
        if isinstance(val, list):
            return val[0] if val else None
        return val
    except Exception:
        pass

    # Older Streamlit
    try:
        qp = st.experimental_get_query_params()
        val = qp.get("answer", [None])[0]
        return val
    except Exception:
        return None

def clear_query_params():
    # Avoid showing ?answer=... after we consume it
    try:
        st.query_params.clear()
    except Exception:
        try:
            st.experimental_set_query_params()
        except Exception:
            pass

# ----------------------------
# State
# ----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "accepted" not in st.session_state:
    st.session_state.accepted = False

# ----------------------------
# UI chunks
# ----------------------------
def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-title">{title}</div>
          <div class="hero-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def glass_open(pill_text: str):
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(f'<div class="pill">{pill_text}</div>', unsafe_allow_html=True)

def glass_close():
    st.markdown("</div>", unsafe_allow_html=True)

def loading_screen():
    hero("A tiny surprise for you 💗", "Made with a stupid amount of love and a tiny bit of nerves.")
    glass_open("Loading something sweet…")

    st.markdown('<div class="shimmer"></div>', unsafe_allow_html=True)
    st.markdown("")

    progress = st.progress(0)
    msg = st.empty()
    lines = [
        "Pinning soft memories to the moodboard… 📌",
        "Stealing a few butterflies… 🦋",
        "Warming up the blush generator… 🌸",
        "Tying a ribbon around the moment… 🎀",
        "Okay… okay… ready. 😳",
    ]
    for i in range(101):
        progress.progress(i)
        if i % 20 == 0 and i // 20 < len(lines):
            msg.markdown(f"**{lines[i//20]}**")
        time.sleep(0.013)

    st.markdown("I’m gonna ask you something now. Be gentle with my heart. 🥺")
    glass_close()

def step_card(pill_text: str, body_md: str):
    glass_open(pill_text)
    st.markdown(body_md)
    glass_close()

def go_next():
    st.session_state.step += 1

# ----------------------------
# Handle YES from the HTML component (query param)
# ----------------------------
answer = get_answer_param()
if answer == "yes":
    st.session_state.accepted = True
    st.session_state.step = max(st.session_state.step, 5)
    clear_query_params()

# ----------------------------
# App flow
# ----------------------------
if st.session_state.step == 0:
    loading_screen()
    if st.button("Open it 💌"):
        go_next()
        st.rerun()

elif st.session_state.step == 1:
    hero("Okay… hi. 😳", "Not gonna be cringe. (I’m lying a little.)")
    step_card(
        "A soft confession",
        """
Some people feel like sunshine.

You feel like **home** — the kind that’s warm, safe, and instantly makes the world quieter.

And I wanted to do something that feels like *us*: cute, a bit shy, and very real.
""",
    )
    if st.button("Keep going 🥺"):
        go_next()
        st.rerun()

elif st.session_state.step == 2:
    hero("Quick vibe check ✨", "If you had to pick…")
    step_card(
        "Choose our mood",
        """
- Cozy date + snacks + your laugh  
- A cute little walk + holding hands  
- Staying in + being stupid together  

**(I love all three. With you, anything wins.)**
""",
    )
    if st.button("Okay okay… next 💞"):
        go_next()
        st.rerun()

elif st.session_state.step == 3:
    hero("Deep breath 😮‍💨", "Here comes the actual question…")
    step_card(
        "Promise I’ll be brave",
        """
I’m asking this properly because you deserve a moment you can smile at.

So… Buchu…
""",
    )
    if st.button("ASK 😤💗"):
        go_next()
        st.rerun()

elif st.session_state.step == 4:
    hero("Buchu 💘", "Will you be my Valentine?")
    step_card(
        "Pick your answer (carefully 😌)",
        "I made the **No** button… a little shy.",
    )

    # HTML component: yes sets query param, no runs away + shrinks + vanishes
    components.html(
        """
        <div style="
            margin-top: 14px;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(255, 105, 180, 0.22);
            border-radius: 22px;
            padding: 18px;
            box-shadow: 0 20px 70px rgba(255, 105, 180, 0.12), 0 12px 40px rgba(60, 120, 255, 0.08);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
        ">
          <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
            <button id="yesBtn"
              style="
                cursor:pointer;
                border-radius: 18px;
                padding: 14px 18px;
                font-size: 16px;
                font-weight: 800;
                border: 1px solid rgba(255, 105, 180, 0.22);
                background: linear-gradient(135deg, rgba(255,105,180,0.22), rgba(173,216,230,0.16), rgba(255,255,255,0.55));
                box-shadow: 0 12px 30px rgba(255, 105, 180, 0.10);
                min-width: 180px;
              "
            >Yes 💖</button>

            <button id="noBtn"
              style="
                position: relative;
                cursor:pointer;
                border-radius: 18px;
                padding: 14px 18px;
                font-size: 16px;
                font-weight: 800;
                border: 1px solid rgba(25,20,30,0.12);
                background: rgba(255,255,255,0.65);
                box-shadow: 0 10px 24px rgba(25,20,30,0.06);
                min-width: 180px;
                transition: transform 0.18s ease, opacity 0.18s ease;
              "
            >No 🙃</button>
          </div>

          <div id="tinyNote" style="margin-top:14px; text-align:center; color: rgba(25,20,30,0.58); font-size: 13.5px;">
            If the “No” button moves… that’s not a bug. That’s my self-respect. 😭
          </div>
        </div>

        <script>
          const yesBtn = document.getElementById("yesBtn");
          const noBtn  = document.getElementById("noBtn");

          function moveNoButton() {
            const dx = (Math.random() * 260) - 130; // -130..130
            const dy = (Math.random() * 180) - 90;  // -90..90
            noBtn.style.transform = `translate(${dx}px, ${dy}px) scale(0.95)`;
          }

          noBtn.addEventListener("mouseenter", () => {
            moveNoButton();
          });

          noBtn.addEventListener("click", () => {
            // Shrink + vanish
            noBtn.style.transform = "scale(0.2)";
            noBtn.style.opacity = "0";
            setTimeout(() => {
              noBtn.style.display = "none";
              document.getElementById("tinyNote").innerText =
                "No option removed for your convenience. You're welcome. 😌💗";
            }, 220);
          });

          yesBtn.addEventListener("click", () => {
            // Navigate with query param so Streamlit can read it reliably
            const url = new URL(window.location.href);
            url.searchParams.set("answer", "yes");
            window.location.href = url.toString();
          });
        </script>
        """,
        height=240,
    )

    st.markdown('<div class="tiny">Tip: hover the No button 😭</div>', unsafe_allow_html=True)

elif st.session_state.step == 5:
    hero("YOU SAID YES 😭💗", "Okay I’m actually so happy.")
    st.balloons()

    step_card(
        "One last thing…",
        """
Before we go plan the cutest Valentine’s Day ever,
I wrote you something.
""",
    )
    if st.button("Open the letter 💌"):
        go_next()
        st.rerun()

else:
    hero("A letter for you, Buchu 💌", "Keep this. It’s yours.")
    glass_open("From my heart, to you")

    st.markdown(
        """
<div class="letter">
<p><b>My Buchu,</b></p>

<p>
I don’t know when it happened exactly, but you slowly became the sweetest part of my day.
You make ordinary moments feel softer — like life is kinder when you’re in it.
</p>

<p>
I love you. In the real way.
The way I want to tell you everything.
The way I notice the tiniest things about you.
The way your happiness genuinely matters to me.
</p>

<p>
If you’ll be my Valentine, I want it to feel like us:
cozy, cute, and full of those little looks that say “I’m glad it’s you.”
I’ll hold your hand, hype you up, annoy you a little (for balance),
and keep choosing you — not just on Valentine’s Day, but on all the random days too.
</p>

<p>
Thank you for being you.
Thank you for letting me love you.
</p>

<p class="signature">
Yours,<br>
Tanmay 💗
</p>
</div>
        """,
        unsafe_allow_html=True,
    )
    glass_close()

    st.markdown("")
    if st.button("Restart (because watching you smile is my favorite) 🔁"):
        st.session_state.step = 0
        st.session_state.accepted = False
        clear_query_params()
        st.rerun()
