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
# Aesthetic + animated background (Pinterest-y)
# ----------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,750&family=Inter:wght@400;500;600;700&display=swap');

      :root{
        --ink: rgba(25, 20, 30, 0.92);
        --muted: rgba(25, 20, 30, 0.60);
        --card: rgba(255,255,255,0.68);
        --stroke: rgba(255, 105, 180, 0.22);
        --shadow: 0 24px 80px rgba(255, 105, 180, 0.14);
        --shadow2: 0 18px 60px rgba(60, 120, 255, 0.10);
      }

      /* Animated gradient background */
      .stApp{
        background: linear-gradient(120deg,
          #fff6fb 0%,
          #ffeef6 20%,
          #f7fbff 45%,
          #fff8f0 70%,
          #fff6fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 14s ease-in-out infinite;
      }
      @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }

      /* Floating hearts layer */
      .heart-layer{
        pointer-events:none;
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
      }
      .heart{
        position:absolute;
        font-size: 18px;
        opacity: 0.14;
        animation: floatUp linear infinite;
        filter: blur(0.2px);
      }
      @keyframes floatUp{
        from { transform: translateY(110vh) translateX(0) scale(0.9); }
        to   { transform: translateY(-15vh) translateX(40px) scale(1.2); }
      }

      /* Keep content above background */
      .block-container{
        position: relative;
        z-index: 2;
        max-width: 880px;
        padding-top: 2.2rem;
        padding-bottom: 3.4rem;
      }

      header, footer { visibility: hidden; }

      h1, h2, h3, h4, h5, h6 { font-family: "Fraunces", serif !important; color: var(--ink); }
      p, li, div, span { font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Arial !important; color: var(--ink); }

      .hero{
        text-align:center;
        margin: 0.2rem 0 1.2rem 0;
      }
      .hero-title{
        font-family:"Fraunces", serif;
        font-size: 2.75rem;
        line-height: 1.03;
        margin: 0.25rem 0 0.35rem 0;
        letter-spacing: -0.8px;
      }
      .hero-sub{
        font-size: 1.06rem;
        color: var(--muted);
        margin: 0;
      }

      .glass{
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: 24px;
        padding: 1.25rem 1.25rem;
        box-shadow: var(--shadow), var(--shadow2);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
      }

      .pill{
        display:inline-block;
        padding: 0.34rem 0.78rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 105, 180, 0.18);
        background: rgba(255, 182, 193, 0.22);
        color: rgba(25, 20, 30, 0.78);
        font-size: 0.92rem;
        margin-bottom: 0.85rem;
      }

      .shimmer{
        height: 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.62);
        border: 1px solid rgba(255, 105, 180, 0.16);
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(255, 105, 180, 0.10);
      }
      .shimmer::before{
        content:"";
        display:block;
        height:100%;
        width:42%;
        background: linear-gradient(90deg,
          rgba(255,105,180,0.0),
          rgba(255,105,180,0.24),
          rgba(173,216,230,0.20),
          rgba(255,105,180,0.0));
        animation: shine 1.15s infinite;
      }
      @keyframes shine{
        0% { transform: translateX(-70%); }
        100% { transform: translateX(280%); }
      }

      div.stButton > button{
        width: 100%;
        border-radius: 18px;
        padding: 0.9rem 1rem;
        font-size: 1.05rem;
        font-weight: 800;
        border: 1px solid rgba(255, 105, 180, 0.22);
        background: linear-gradient(135deg,
          rgba(255,105,180,0.22),
          rgba(173,216,230,0.14),
          rgba(255,255,255,0.55));
        box-shadow: 0 14px 36px rgba(255, 105, 180, 0.12);
      }
      div.stButton > button:hover{
        transform: translateY(-1px);
        border: 1px solid rgba(255, 105, 180, 0.34);
      }

      .letter{
        line-height: 1.75;
        font-size: 1.06rem;
      }
      .signature{
        margin-top: 1.0rem;
        font-weight: 800;
      }
      .tiny{
        color: var(--muted);
        font-size: 0.95rem;
        text-align: center;
        margin-top: 0.85rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hearts overlay (pure HTML, no JS needed)
st.markdown(
    """
    <div class="heart-layer">
      <span class="heart" style="left:8%;  animation-duration: 14s; animation-delay:-2s;">💗</span>
      <span class="heart" style="left:18%; animation-duration: 18s; animation-delay:-6s;">💖</span>
      <span class="heart" style="left:28%; animation-duration: 16s; animation-delay:-9s;">💘</span>
      <span class="heart" style="left:40%; animation-duration: 20s; animation-delay:-4s;">💞</span>
      <span class="heart" style="left:52%; animation-duration: 15s; animation-delay:-7s;">💝</span>
      <span class="heart" style="left:64%; animation-duration: 19s; animation-delay:-11s;">💓</span>
      <span class="heart" style="left:76%; animation-duration: 17s; animation-delay:-5s;">💗</span>
      <span class="heart" style="left:88%; animation-duration: 21s; animation-delay:-10s;">💖</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Query param helper
# ----------------------------
def get_answer_param():
    try:
        qp = st.query_params
        val = qp.get("answer")
        if isinstance(val, list):
            return val[0] if val else None
        return val
    except Exception:
        try:
            qp = st.experimental_get_query_params()
            return qp.get("answer", [None])[0]
        except Exception:
            return None

def clear_query_params():
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

# If user clicked YES in the HTML component, parent URL gets ?answer=yes
ans = get_answer_param()
if ans == "yes":
    st.session_state.accepted = True
    st.session_state.step = 5
    clear_query_params()

# ----------------------------
# UI helpers
# ----------------------------
def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-title">{title}</div>
          <div class="hero-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def glass_open(pill_text):
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(f'<div class="pill">{pill_text}</div>', unsafe_allow_html=True)

def glass_close():
    st.markdown("</div>", unsafe_allow_html=True)

def step_card(pill_text, body_md):
    glass_open(pill_text)
    st.markdown(body_md)
    glass_close()

def loading_screen():
    hero("A tiny surprise 💌", "Soft, sweet, and made just for you.")
    glass_open("Loading… but make it cute")
    st.markdown('<div class="shimmer"></div>', unsafe_allow_html=True)
    st.markdown("")
    progress = st.progress(0)
    msg = st.empty()
    lines = [
        "Pinning the moodboard… 📌",
        "Borrowing butterflies… 🦋",
        "Starting the blush engine… 🌸",
        "Wrapping the moment in ribbon… 🎀",
        "Okay… ready. 😳",
    ]
    for i in range(101):
        progress.progress(i)
        if i % 20 == 0 and i // 20 < len(lines):
            msg.markdown(f"**{lines[i//20]}**")
        time.sleep(0.012)
    st.markdown("Alright… I’m gonna ask you something now. Be gentle. 🥺")
    glass_close()

def go_next():
    st.session_state.step += 1

# ----------------------------
# App flow
# ----------------------------
if st.session_state.step == 0:
    loading_screen()
    if st.button("Open it 💗"):
        go_next()
        st.rerun()

elif st.session_state.step == 1:
    hero("Hi Buchu 😳", "I’m trying to be brave for one second.")
    step_card(
        "A soft little truth",
        """
You make my days feel lighter.

Not in a loud way — in a calm, safe, *I can breathe* kind of way.

So I made this… because you deserve a moment that feels special.
""",
    )
    if st.button("Okay… keep going 💞"):
        go_next()
        st.rerun()

elif st.session_state.step == 2:
    hero("Tiny vibe check ✨", "Pick our energy.")
    step_card(
        "Choose the mood",
        """
- Cozy date + snacks + your laugh  
- Cute walk + warm hands  
- Staying in + being silly together  

**With you, every option is the right one.**
""",
    )
    if st.button("Next 😤💗"):
        go_next()
        st.rerun()

elif st.session_state.step == 3:
    hero("Deep breath 😮‍💨", "Here comes the question…")
    step_card(
        "I mean it",
        """
Buchu… I like you in a way that feels steady.

Like I don’t just want a moment —
I want **more moments**.
""",
    )
    if st.button("ASK ME 🥺"):
        go_next()
        st.rerun()

elif st.session_state.step == 4:
    hero("Buchu 💘", "Will you be my Valentine?")
    step_card("Choose carefully 😌", "The **No** button is… emotionally unavailable.")

    # Working HTML: uses window.parent.location (fixes the YES bug)
    # Working NO: absolute positioning inside a bounded arena + vanish on click
    components.html(
        """
        <div id="arena" style="
          position: relative;
          height: 210px;
          border-radius: 22px;
          background: rgba(255,255,255,0.55);
          border: 1px solid rgba(255, 105, 180, 0.18);
          box-shadow: 0 20px 70px rgba(255, 105, 180, 0.12), 0 12px 40px rgba(60, 120, 255, 0.08);
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
          overflow: hidden;
          padding: 16px;
        ">
          <div style="text-align:center; font-weight:700; color: rgba(25,20,30,0.65); margin-bottom: 10px;">
            Try clicking “No” if you dare 😭
          </div>

          <button id="yesBtn" style="
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            bottom: 18px;
            cursor: pointer;
            border-radius: 18px;
            padding: 14px 18px;
            font-size: 16px;
            font-weight: 900;
            border: 1px solid rgba(255, 105, 180, 0.22);
            background: linear-gradient(135deg, rgba(255,105,180,0.24), rgba(173,216,230,0.16), rgba(255,255,255,0.6));
            box-shadow: 0 12px 30px rgba(255, 105, 180, 0.12);
            min-width: 190px;
          ">Yes 💖</button>

          <button id="noBtn" style="
            position: absolute;
            left: 12%;
            top: 70px;
            cursor: pointer;
            border-radius: 18px;
            padding: 14px 18px;
            font-size: 16px;
            font-weight: 900;
            border: 1px solid rgba(25,20,30,0.12);
            background: rgba(255,255,255,0.70);
            box-shadow: 0 10px 24px rgba(25,20,30,0.07);
            min-width: 190px;
            transition: transform 0.16s ease, opacity 0.16s ease;
          ">No 🙃</button>

          <div id="note" style="
            position:absolute;
            left: 0;
            right: 0;
            bottom: 70px;
            text-align:center;
            color: rgba(25,20,30,0.55);
            font-size: 13.5px;
          ">
            (Not a bug. I trained it to protect my feelings.)
          </div>
        </div>

        <script>
          const arena = document.getElementById("arena");
          const noBtn = document.getElementById("noBtn");
          const yesBtn = document.getElementById("yesBtn");
          const note = document.getElementById("note");

          function rand(min, max){ return Math.random() * (max - min) + min; }

          function moveNo(){
            const arenaRect = arena.getBoundingClientRect();
            const btnRect = noBtn.getBoundingClientRect();

            const padding = 10;
            const maxX = arenaRect.width - btnRect.width - padding;
            const maxY = arenaRect.height - btnRect.height - 60; // keep above note/yes area

            const x = rand(padding, Math.max(padding, maxX));
            const y = rand(52, Math.max(52, maxY));

            noBtn.style.left = x + "px";
            noBtn.style.top = y + "px";
            noBtn.style.transform = "scale(0.97)";
            setTimeout(() => { noBtn.style.transform = "scale(1)"; }, 120);
          }

          noBtn.addEventListener("mouseenter", moveNo);
          noBtn.addEventListener("mousedown", moveNo);
          noBtn.addEventListener("click", () => {
            noBtn.style.transform = "scale(0.2)";
            noBtn.style.opacity = "0";
            setTimeout(() => {
              noBtn.style.display = "none";
              note.textContent = "No option has been removed for your convenience. 😌💗";
            }, 170);
          });

          yesBtn.addEventListener("click", () => {
            // IMPORTANT: update the PARENT page URL (not the iframe)
            const url = new URL(window.parent.location.href);
            url.searchParams.set("answer", "yes");
            window.parent.location.href = url.toString();
          });
        </script>
        """,
        height=250,
    )

    st.markdown('<div class="tiny">Hover the “No” button 🤭</div>', unsafe_allow_html=True)

elif st.session_state.step == 5:
    hero("YOU SAID YES 😭💗", "Okay I’m actually so, so happy.")
    st.balloons()

    step_card(
        "One last thing…",
        """
I wrote you a letter, Buchu.

Like a real one.
The kind you keep.
""",
    )
    if st.button("Open the letter 💌"):
        go_next()
        st.rerun()

else:
    hero("For Buchu 💌", "From me, with everything I feel.")
    glass_open("A letter")

    st.markdown(
        """
<div class="letter">
<p><b>My Buchu,</b></p>

<p>
I don’t know exactly when it started, but somewhere along the way you became my favorite part of the day.
It’s not even always the big moments — it’s the small ones.
The way you exist in my world makes it softer.
</p>

<p>
I love you.
Not in a dramatic, perfect-story kind of way —
in the real way.
The way I want to tell you everything.
The way I care about how you’re feeling.
The way I catch myself smiling because I remembered something you said.
</p>

<p>
If you’ll be my Valentine, I want it to feel like us:
cute, cozy, and full of those little quiet moments that mean more than they should.
I’ll hold your hand, protect your heart, hype you up,
and keep choosing you — not just on Valentine’s Day,
but on all the random days too.
</p>

<p>
Thank you for being you.
Thank you for letting me love you.
I’m really, really grateful it’s you.
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
    if st.button("Restart 🔁"):
        st.session_state.step = 0
        st.session_state.accepted = False
        clear_query_params()
        st.rerun()
