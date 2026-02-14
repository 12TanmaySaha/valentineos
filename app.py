import streamlit as st
import time

GF_NAME   = "Dipika"
YOUR_NAME = "Tanmay"

st.set_page_config(page_title="PookieBear 💗", page_icon="🐱", layout="centered")

# ---------------------------------
# PINK AESTHETIC + CATS + HEARTS
# ---------------------------------
st.markdown("""
<style>
.stApp{
background:linear-gradient(180deg,#fff0f6,#ffe4ec,#ffd6e7);
color:#ff4d8d;
font-family: "Comic Sans MS", cursive;
}

/* floating hearts */
@keyframes float {
0%{transform:translateY(0);opacity:0}
20%{opacity:1}
100%{transform:translateY(-600px);opacity:0}
}
.heart{
position:fixed;
bottom:-40px;
font-size:24px;
animation:float linear infinite;
}
.h1{left:10%;animation-duration:8s}
.h2{left:30%;animation-duration:10s}
.h3{left:50%;animation-duration:7s}
.h4{left:70%;animation-duration:11s}
.h5{left:90%;animation-duration:9s}

/* floating cats */
@keyframes catfloat {
0%{transform:translateY(20px) rotate(0deg)}
50%{transform:translateY(-20px) rotate(5deg)}
100%{transform:translateY(20px) rotate(0deg)}
}
.cat{
position:fixed;
font-size:40px;
animation:catfloat 4s ease-in-out infinite;
}
.c1{left:5%;top:20%}
.c2{right:6%;top:25%}
.c3{left:10%;bottom:20%}
.c4{right:10%;bottom:18%}

/* card */
.card{
background:white;
padding:25px;
border-radius:25px;
box-shadow:0 10px 30px rgba(255,105,180,.25);
text-align:center;
}

/* yes button */
.yes button{
background:#ff6fa8 !important;
color:white !important;
font-size:22px !important;
height:65px !important;
border-radius:20px !important;
font-weight:900 !important;
}
</style>

<div class="heart h1">💗</div>
<div class="heart h2">💖</div>
<div class="heart h3">💞</div>
<div class="heart h4">💕</div>
<div class="heart h5">💓</div>

<div class="cat c1">🐱</div>
<div class="cat c2">😺</div>
<div class="cat c3">🐈</div>
<div class="cat c4">🐈‍⬛</div>
""",unsafe_allow_html=True)

# ---------------------------------
# BOOT
# ---------------------------------
if "stage" not in st.session_state:
    st.session_state.stage="boot"

if st.session_state.stage=="boot":
    st.markdown(f"""
    <div class="card">
    <h1>PookieBearOS 🐱💗</h1>
    <p>loading cuddles for {GF_NAME}...</p>
    </div>
    """,unsafe_allow_html=True)

    bar=st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        bar.progress(i+1)

    if st.button("enter 💌"):
        st.session_state.stage="question"
        st.rerun()

# ---------------------------------
# QUESTION SCREEN
# ---------------------------------
elif st.session_state.stage=="question":

    st.markdown(f"""
    <div class="card">
    <h1>{GF_NAME} 💕</h1>
    <h2>Will you be my Valentine?</h2>
    </div>
    """,unsafe_allow_html=True)

    # YES button
    st.markdown('<div class="yes">',unsafe_allow_html=True)
    if st.button("YES 💖"):
        st.session_state.stage="yes"
        st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

    # CHAOTIC NO BUTTON (REAL MOVEMENT)
    st.components.v1.html("""
    <div style="position:relative;height:200px;">
        <button id="noBtn" style="
        position:absolute;
        left:40%;
        top:60%;
        padding:15px 25px;
        font-size:20px;
        border-radius:20px;
        border:none;
        background:#ffc2d6;
        font-weight:800;
        cursor:pointer;">NO 🙃</button>
    </div>

    <script>
    const btn=document.getElementById("noBtn");
    let tries=0;

    function move(){
        const x=Math.random()*80;
        const y=Math.random()*80;
        btn.style.left=x+"%";
        btn.style.top=y+"%";
    }

    btn.onmouseover=move;

    btn.onclick=()=>{
        tries++;

        if(tries==1){btn.innerText="nope";}
        else if(tries==2){btn.innerText="stop 😭";}
        else if(tries==3){btn.innerText="why??";}
        else if(tries==4){btn.innerText="press yes";}
        else if(tries>=5){
            btn.style.display="none";
            alert("NO option removed permanently 💗");
        }
        move();
    };
    </script>
    """,height=220)

# ---------------------------------
# YES SCREEN
# ---------------------------------
else:
    st.balloons()
    st.markdown(f"""
    <div class="card">
    <h1>YAYYYYY 💞🐱</h1>
    <h2>{GF_NAME} you made {YOUR_NAME} the happiest person alive</h2>
    <p>February 14 is ours now 💗</p>
    </div>
    """,unsafe_allow_html=True)
