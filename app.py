import random
import string
import time
from io import BytesIO

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# -----------------------------
# Settings
# -----------------------------
GF_NAME = "Dipika"
YOUR_NAME = "Tanmay"  # change if you want
CAPTCHA_LEN = 5

st.set_page_config(page_title="ValentineOS 💘", page_icon="💘", layout="centered")

# -----------------------------
# Styling (cute UI)
# -----------------------------
st.markdown(
    """
    <style>
      .title {font-size: 44px; font-weight: 900; margin-bottom: 0.2rem;}
      .subtitle {font-size: 18px; opacity: 0.85; margin-top: 0;}
      .card {
        padding: 18px 18px 10px 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.05);
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
      }
      .pill {
        display:inline-block; padding:6px 10px; border-radius:999px;
        border:1px solid rgba(255,255,255,0.18); background: rgba(255,255,255,0.05);
        font-size: 13px; opacity: 0.9;
      }
      .bigbtn button {width: 100%; height: 58px; font-size: 18px; border-radius: 16px;}
      .tiny {font-size: 13px; opacity: 0.75;}
      .center {text-align:center;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def gen_code(n=CAPTCHA_LEN) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(n))

def make_text_captcha_image(code: str, w=520, h=170) -> Image.Image:
    img = Image.new("RGB", (w, h), (20, 20, 28))
    draw = ImageDraw.Draw(img)

    # noise lines
    for _ in range(18):
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2, y2 = random.randint(0, w), random.randint(0, h)
        draw.line((x1, y1, x2, y2), fill=(80, 80, 110), width=random.randint(1, 3))

    # font (fallback safe)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 82)
    except Exception:
        font = ImageFont.load_default()

    # text shadow + text
    text = "  ".join(list(code))
    tw, th = draw.textbbox((0, 0), text, font=font)[2:]
    x = (w - tw) // 2
    y = (h - th) // 2 - 5

    draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # more speckles
    for _ in range(800):
        draw.point((random.randint(0, w - 1), random.randint(0, h - 1)),
                   fill=random.choice([(255, 255, 255), (160, 160, 200), (80, 80, 120)]))

    return img

def overlay_code_on_photo(photo: Image.Image, code: str) -> Image.Image:
    img = photo.convert("RGB")
    w, h = img.size

    # banner at bottom
    banner_h = max(80, h // 6)
    overlay = Image.new("RGBA", (w, banner_h), (0, 0, 0, 150))
    base = img.convert("RGBA")
    base.paste(overlay, (0, h - banner_h), overlay)
    base = base.convert("RGB")

    draw = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", max(28, banner_h // 2))
    except Exception:
        font = ImageFont.load_default()

    text = f"Type this code:  {code}"
    # shadow + text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = h - banner_h + (banner_h - th) // 2
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    return base

def boot_sequence():
    st.markdown(f'<div class="card center"><div class="title">ValentineOS 💘</div>'
                f'<p class="subtitle">Booting love modules for <b>{GF_NAME}</b>…</p></div>',
                unsafe_allow_html=True)
    p = st.progress(0)
    labels = ["Initializing romance.dll", "Compiling feelings.py", "Deploying butterflies.exe", "Launching question.ui"]
    for i, lab in enumerate(labels, start=1):
        st.caption(lab)
        for k in range(25):
            p.progress(min(100, int(((i - 1) * 25 + k) / (len(labels) * 25) * 100)))
            time.sleep(0.02)
    p.progress(100)
    st.success("Boot complete ✅")

# -----------------------------
# Session state
# -----------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "boot"
if "captcha_code" not in st.session_state:
    st.session_state.captcha_code = gen_code()
if "no_count" not in st.session_state:
    st.session_state.no_count = 0

# -----------------------------
# App flow
# -----------------------------
if st.session_state.stage == "boot":
    boot_sequence()
    st.markdown("<div class='center'>✨ 💖 💘 💞 ✨</div>", unsafe_allow_html=True)
    if st.button("Continue ➜"):
        st.session_state.stage = "captcha"
        st.rerun()

elif st.session_state.stage == "captcha":
    st.markdown(
        f"<div class='card'>"
        f"<div class='title'>Human check 🤖➡️🥰</div>"
        f"<p class='subtitle'>{GF_NAME}, prove you’re not a robot so I can ask the important question.</p>"
        f"<span class='pill'>Tip: type exactly what you see</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    colA, colB = st.columns([1, 1], gap="large")
    with colA:
        st.subheader("Option A: Normal CAPTCHA")
        img = make_text_captcha_image(st.session_state.captcha_code)
        st.image(img, use_container_width=True)
    with colB:
        st.subheader("Option B: Photo CAPTCHA (upload)")
        up = st.file_uploader("Upload any photo (jpg/png/webp)", type=["jpg", "jpeg", "png", "webp"])
        if up is not None:
            photo = Image.open(up)
            img2 = overlay_code_on_photo(photo, st.session_state.captcha_code)
            st.image(img2, use_container_width=True)
        st.caption("Privacy: the photo is only used in this session for the overlay.")

    typed = st.text_input("Enter the CAPTCHA code")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Refresh code 🔄"):
            st.session_state.captcha_code = gen_code()
            st.rerun()
    with c2:
        if st.button("Verify ✅"):
            if typed.strip().upper() == st.session_state.captcha_code:
                st.success("Verified 💖")
                st.session_state.stage = "question"
                st.rerun()
            else:
                st.error("Nope 😭 try again (or refresh).")
    with c3:
        st.caption("")

elif st.session_state.stage == "question":
    st.markdown(
        f"<div class='card center'>"
        f"<div class='title'>Dipika… 💌</div>"
        f"<p class='subtitle'>I have one question. (Be honest… but also… choose wisely 😌)</p>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='center'>💖 💘 💞 💖 💘 💞</div>", unsafe_allow_html=True)

    st.markdown(f"<h2 class='center'>Will you be my Valentine?</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='bigbtn'>", unsafe_allow_html=True)
        if st.button("YES 💞"):
            st.session_state.stage = "yes"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='bigbtn'>", unsafe_allow_html=True)
        if st.button("NO 🙃"):
            st.session_state.no_count += 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.no_count > 0:
        excuses = [
            "❌ NO is currently disabled.",
            "👀 That button is decorative.",
            "😤 Nice try. Only YES works today.",
            "💘 Timeline error: 'No' not found.",
            "🤝 Let’s renegotiate that answer 😌",
        ]
        st.warning(excuses[min(st.session_state.no_count - 1, len(excuses) - 1)])
        if st.session_state.no_count >= 5:
            st.info("Okay okay… I’ll ask nicely: Please say yes 😭❤️")

elif st.session_state.stage == "yes":
    st.balloons()
    st.markdown(
        f"<div class='card center'>"
        f"<div class='title'>YAYYYYY 🎉</div>"
        f"<p class='subtitle'><b>{GF_NAME}</b>, you just made <b>{YOUR_NAME}</b> the happiest person ❤️</p>"
        f"<p>📅 Date scheduled: Feb 14 (all day)</p>"
        f"<p>🍫 Optional add-ons: chocolate, flowers, unlimited attention</p>"
        f"<p class='tiny'>PS: Screenshot this and send it to me 😌</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.button("Replay 🔁"):
        st.session_state.stage = "boot"
        st.session_state.no_count = 0
        st.session_state.captcha_code = gen_code()
        st.rerun()


