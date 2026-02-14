import time
import streamlit as st

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Buchu, will you be my Valentine? 💘",
    page_icon="💝",
    layout="centered",
)

# ----------------------------
# Cute CSS theme (soft, pretty, readable)
# ----------------------------
st.markdown(
    """
    <style>
      /* App background */
      .stApp {
        background: radial-gradient(circle at 20% 10%, rgba(255, 209, 220, 0.55) 0%, rgba(255,255,255,0.9) 40%, rgba(255, 242, 247, 1) 100%);
      }

      /* Center main container a bit */
      .block-container {
        max-width: 820px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
      }

      /* Title styling */
      .cute-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-align: center;
        margin: 0.6rem 0 0.2rem 0;
      }

      .cute-subtitle {
        text-align: center;
        font-size: 1.1rem;
        opacity: 0.85;
        margin-bottom: 1.6rem;
      }

      /* Card */
      .card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 192, 203, 0.55);
        border-radius: 18px;
        padding: 1.2rem 1.2rem;
        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.08);
        margin: 0.9rem 0;
      }

      /* Badge */
      .badge {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        background: rgba(255, 182, 193, 0.35);
        border: 1px solid rgba(255, 105, 180, 0.25);
        font-size: 0.95rem;
        margin-bottom: 0.65rem;
      }

      /* Letter */
      .letter {
        background: rgba(255,255,255,0.88);
        border-radius: 18px;
        padding: 1.3rem 1.3rem;
        border: 1px solid rgba(255, 105, 180, 0.22);
        box-shadow: 0 12px 40px rgba(255, 105, 180, 0.08);
        line-height: 1.65;
        font-size: 1.03rem;
      }

      /* Button */
      div.stButton > button {
        width: 100%;
        border-radius: 16px;
        padding: 0.85rem 1rem;
        font-size: 1.05rem;
        font-weight: 700;
        border: 1px solid rgba(255, 105, 180, 0.25);
        background: linear-gradient(135deg, rgba(255,105,180,0.20), rgba(255,182,193,0.35));
      }
      div.stButton > button:hover {
        border: 1px solid rgba(255, 105, 180, 0.45);
        transform: translateY(-1px);
      }

      /* Tiny hearts animation */
      .hearts {
        text-align: center;
        font-size: 1.3rem;
        margin: 0.4rem 0 0.6rem 0;
        animation: floaty 2.5s ease-in-out infinite;
      }
      @keyframes floaty {
        0%, 100% { transform: translateY(0px); opacity: 0.95; }
        50% { transform: translateY(-6px); opacity: 1; }
      }

      /* Hide Streamlit footer */
      footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Session state defaults
# ----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "accepted" not in st.session_state:
    st.session_state.accepted = False

# ----------------------------
# Helpers
# ----------------------------
def cute_header():
    st.markdown('<div class="cute-title">Hey Buchu 💘</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cute-subtitle">I made a tiny little page… because asking you normally wasn’t enough 🥺</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hearts">💗 💞 💖 💘 💝</div>', unsafe_allow_html=True)

def loading_screen():
    cute_header()
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="badge">Loading something cute…</div>', unsafe_allow_html=True)

    progress = st.progress(0)
    messages = [
        "Collecting butterflies… 🦋",
        "Warming up the heart machine… 💓",
        "Practicing my shy smile… 😳",
        "Wrapping a little surprise… 🎀",
        "Almost there… ✨",
    ]
    msg = st.empty()

    for i in range(101):
        progress.progress(i)
        if i % 20 == 0 and i // 20 < len(messages):
            msg.markdown(f"**{messages[i//20]}**")
        time.sleep(0.015)

    st.markdown("Done. Okay… deep breath. 😮‍💨", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def step_card(title, body):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="badge">{title}</div>', unsafe_allow_html=True)
    st.markdown(body)
    st.markdown("</div>", unsafe_allow_html=True)

def go_next():
    st.session_state.step += 1

# ----------------------------
# App flow
# ----------------------------
cute_header()

if st.session_state.step == 0:
    loading_screen()
    if st.button("Okay Buchu, show me 💝"):
        go_next()
        st.rerun()

elif st.session_state.step == 1:
    step_card(
        "Tiny confession 🤏",
        """
I’ve been carrying this soft little feeling for you that makes ordinary days feel… less ordinary.

Like, somehow, everything is cuter when you’re in my world.
""",
    )
    if st.button("Aww. Keep going 🥺"):
        go_next()
        st.rerun()

elif st.session_state.step == 2:
    step_card(
        "Quick quiz (very serious) 📝",
        """
**Which option sounds most like us?**

- Cozy vibes + snacks + your smile  
- A cute date + random laughs  
- All of the above (because obviously)  
""",
    )
    if st.button("All of the above ✅"):
        go_next()
        st.rerun()

elif st.session_state.step == 3:
    step_card(
        "Okay… here it comes 😳",
        """
Buchu… I wanted to ask you in a way you’d remember.

Not with a boring text.  
Not with a rushed “hey btw…”

But with something small, sweet, and made for **you**.
""",
    )
    if st.button("Ask me already 😤💗"):
        go_next()
        st.rerun()

elif st.session_state.step == 4:
    step_card(
        "The question 💘",
        """
### Buchu, will you be my Valentine? 🌹
Pick the answer your heart wants.
""",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes 💖"):
            st.session_state.accepted = True
            go_next()
            st.rerun()
    with col2:
        if st.button("Also yes (obviously) 💝"):
            st.session_state.accepted = True
            go_next()
            st.rerun()

elif st.session_state.step == 5:
    if st.session_state.accepted:
        st.balloons()
        step_card(
            "EEEEEE 😭💗",
            """
You just made my heart do a full gymnastics routine.

I’m so happy it’s you.
""",
        )
    else:
        step_card(
            "Wait… what? 😳",
            """
I think the universe glitched because this app only supports **YES**.

(Okay but for real… you mean the world to me.)
""",
        )

    if st.button("Open the letter 💌"):
        go_next()
        st.rerun()

else:
    st.markdown(
        """
        <div class="letter">
        <div class="badge">A letter for you, Buchu 💌</div>
        <p>
        My Buchu,<br><br>
        I don’t know how you do it, but you’ve become the softest part of my day.
        When I think about you, I feel calmer… like life makes more sense.
        </p>
        <p>
        I love you — not in a dramatic movie way — but in the quiet, real way:
        the way I miss you when you’re not around,
        the way I want to tell you every little thing,
        the way your happiness matters to me.
        </p>
        <p>
        If you’ll be my Valentine, I want it to be simple:
        more us, more laughs, more warmth, more memories.
        I’ll hold your hand, hype you up, and keep choosing you —
        on Valentine’s Day and on all the random days too.
        </p>
        <p>
        Yours,<br>
        <b>Tanmay</b> 💗
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")
    if st.button("Restart (so I can watch you smile again) 🔁"):
        st.session_state.step = 0
        st.session_state.accepted = False
        st.rerun()
