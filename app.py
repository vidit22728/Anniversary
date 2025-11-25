import streamlit as st
import time
import os
import base64
from PIL import Image
import streamlit.components.v1 as components

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Anniversary Surprise",
    page_icon="💖",
    layout="centered"
)

# ----------------- CONSTANTS -----------------
IMAGE_PATH = r"C:\Users\WELCOME\Downloads\WhatsApp Image 2025-11-24 at 4.36.14 PM.jpeg"

SEQUENCE = ["Greeting Card", "Photo Gallery", "Family Wishes", "Fun Game", "Scratch Cards"]

# Gallery – abhi same image 3 baar; tum yahan alag paths bhi daal sakte ho
GALLERY_IMAGES = [
    IMAGE_PATH,
    IMAGE_PATH,
    IMAGE_PATH,
]

# ----------------- SESSION STATE -----------------
if "view" not in st.session_state:
    st.session_state.view = "start"          # "start", "wheel", "greeting", "gallery", "family", "game", "scratch"

if "scratch_revealed" not in st.session_state:
    st.session_state.scratch_revealed = None

if "redeemed" not in st.session_state:
    st.session_state.redeemed = False

if "spin_animation" not in st.session_state:
    st.session_state.spin_animation = False  # wheel abhi animate ho raha hai ya nahi

if "next_view_after_spin" not in st.session_state:
    st.session_state.next_view_after_spin = None

if "result_index" not in st.session_state:
    st.session_state.result_index = 0        # sequence me ab tak kitne options ho chuke

if "card_open" not in st.session_state:
    st.session_state.card_open = False       # greeting card open hai ya nahi

# ----------------- GLOBAL CSS -----------------
st.markdown(
    """
    <style>
    html, body, .stApp {
    zoom: 0.95; /* Adjust zoom between 1.2 – 1.5 depending on laptop screen */
    transform-origin: top center;
}

    .stApp {
        background: radial-gradient(circle at top, #ff4b4b 0%, #b30000 50%, #4d0000 100%);
        color: #fff;
        overflow-x: hidden;
    }

    /* floating hearts */
    .hearts {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    .heart {
        position: absolute;
        bottom: -60px;
        color: rgba(255,255,255,0.85);
        font-size: 26px;
        animation: floatUp 12s linear infinite;
    }
    .heart:nth-child(2) { left: 15%; animation-duration: 10s; font-size: 22px;}
    .heart:nth-child(3) { left: 35%; animation-duration: 14s; font-size: 32px;}
    .heart:nth-child(4) { left: 65%; animation-duration: 11s; font-size: 24px;}
    .heart:nth-child(5) { left: 85%; animation-duration: 15s; font-size: 30px;}

    @keyframes floatUp {
        0%   { transform: translateY(0) scale(1); opacity: 0; }
        10%  { opacity: 1; }
        100% { transform: translateY(-110vh) scale(1.3); opacity: 0; }
    }

    /* START TITLE */
    .main-title {
        font-size: 110px !important;
        font-weight: 900;
        text-align: center;
        margin-top: 60px;
        color: #ffffff;
        text-shadow: 0 0 18px rgba(0,0,0,0.6);
        letter-spacing: 3px;
    }

    .start-btn button {
        font-size: 60px !important;
        padding: 14px 70px !important;
        border-radius: 20px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg,#ff3b7a,#ff8e8e) !important;
        color: white !important;
        border: 2px solid #ff4b4b !important;
        box-shadow: 0 0 22px rgba(255,50,70,0.9);
    }

    .names-under {
        margin-top: 14px;
        text-align: center;
        font-size: 50px;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 0 12px rgba(0,0,0,0.6);
    }

    /* WHEEL PAGE */
    .wheel-title-main {
        font-size: 85px;
        font-weight: 900;
        text-align: center;
        margin-top: 25px;
        color: white;
        text-shadow: 0 0 18px rgba(0,0,0,0.8);
    }
    .wheel-subtitle {
        text-align: center;
        color: #ffeef4;
        font-size: 24px;
        margin-bottom: 6px;
    }
    .wheel-title-sub {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .wheel-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        position: relative;
    }
    .wheel-pointer {
        width: 0;
        height: 0;
        border-left: 22px solid transparent;
        border-right: 22px solid transparent;
        border-bottom: 36px solid #ffffff;
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        filter: drop-shadow(0 0 8px rgba(0,0,0,0.8));
        z-index: 2;
    }

    .wheel {
        width: 380px;
        height: 380px;
        border-radius: 50%;
        border: 4px solid #fff;
        background: conic-gradient(
            #73e0a9 0deg 72deg,
            #ff6f91 72deg 144deg,
            #ffd56b 144deg 216deg,
            #9ad0ff 216deg 288deg,
            #c77dff 288deg 360deg
        );
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 30px rgba(0,0,0,0.6);
        transition: transform 3s ease-out;
        position: relative;
        margin: 0 auto;
    }

    /* decelerating spin animation */
    @keyframes spinDecel {
        0%   { transform: rotate(0deg);   }
        70%  { transform: rotate(900deg); }
        100% { transform: rotate(1080deg);}
    }
    .wheel.spin {
        animation: spinDecel 3s ease-out forwards;
    }

    .wheel-center {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle,#ffeaf2 0%,#ff9aa2 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #7a0033;
        font-weight: 800;
        font-size: 18px;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.4);
        z-index: 1;
        padding: 10px;
    }

    .wheel-label {
        position: absolute;
        font-size: 14px;
        font-weight: 800;
        color: #fff;
        background: rgba(0,0,0,0.45);
        padding: 4px 10px;
        border-radius: 999px;
        text-shadow: 0 0 6px rgba(0,0,0,0.8);
    }
    .wheel-label.gc { top: 18px; left: 50%; transform: translateX(-50%); }
    .wheel-label.pg { top: 115px; right: 18px; }
    .wheel-label.fw { bottom: 60px; right: 60px; }
    .wheel-label.fg { bottom: 60px; left: 60px; }
    .wheel-label.sc { top: 115px; left: 18px; }

    .spin-btn button {
        font-size: 32px !important;
        padding: 10px 30px !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg,#ff3b7a,#ff8e8e) !important;
        color: #fff !important;
    }

    /* GREETING CARD */
    .greeting-title {
        text-align: center;
        font-size: 80px;
        font-weight: 900;
        margin-top: 20px;
        color: #fff;
        text-shadow: 0 0 18px rgba(0,0,0,0.8);
    }

    .greeting-card-closed {
        margin-top: 40px;
        margin-bottom: 25px;
        background: linear-gradient(135deg,#ffdde1,#ee9ca7);
        padding: 40px 60px;
        text-align: center;
        border-radius: 22px;
        color: #7a0033;
        font-weight: 800;
        font-size: 26px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
    }

    .greeting-text-box {
        background: #fff;
        border-radius: 18px;
        padding: 24px 32px;
        color: #5a0030;
        font-family: Georgia, serif;
        font-size: 18px;
        line-height: 1.7;
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
    }

    .center-btn button {
        font-size: 20px !important;
        padding: 8px 26px !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
    }

    /* GALLERY */
    .gallery-title {
        text-align:center;
        font-size:75px;
        font-weight:900;
        margin-top:20px;
        color:#fff;
        text-shadow:0 0 18px rgba(0,0,0,0.8);
    }
    </style>

    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* Hide wheel while in gallery view */
    .wheel-wrapper {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("""
<div class="hearts">
  <span class="heart">💖</span>
  <span class="heart">💕</span>
  <span class="heart">💗</span>
  <span class="heart">💞</span>
  <span class="heart">❤️</span>
</div>
""", unsafe_allow_html=True)

# ----------------- BACKGROUND MUSIC FUNCTION -----------------
def play_music(path):
    try:
        with open(path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    except:
        pass

# ----------------- VIEWS -----------------

def view_start():
    st.markdown("<div class='main-title'>Anniversary Surprise</div>", unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[1]:
        st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
        if st.button("Start 💖", use_container_width=True):
            st.session_state.view = "wheel"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='names-under'>Shreyas &amp; Prateeksha<br>28/11/2024</div>",
        unsafe_allow_html=True,
    )


def view_wheel():
    # agar animation chal rahi hai to 3 sec ke baad redirect
    if st.session_state.spin_animation and st.session_state.next_view_after_spin:
        # wheel page render hoga, animation front-end pe chalegi,
        # fir 3 sec block karke view change kar denge
        time.sleep(3)
        st.session_state.spin_animation = False
        st.session_state.view = st.session_state.next_view_after_spin
        st.session_state.next_view_after_spin = None
        st.rerun()

    st.markdown("<div class='wheel-title-main'>SPIN THE WHEEL</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='wheel-subtitle'>HAPPY 1ST ANNIVERSARY TO BOTH OF YOU</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='wheel-title-sub'>SPIN THE WHEEL FUN</div>", unsafe_allow_html=True)

    spin_class = "wheel"
    if st.session_state.spin_animation:
        spin_class += " spin"

    # wheel
    st.markdown("<div class='wheel-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='wheel-pointer'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="{spin_class}">
            <div class="wheel-label gc">Greeting Card</div>
            <div class="wheel-label pg">Photo Gallery</div>
            <div class="wheel-label fw">Family Wishes</div>
            <div class="wheel-label fg">Fun Game</div>
            <div class="wheel-label sc">Scratch Cards</div>
            <div class="wheel-center">
                Spin &amp;<br/>See Your<br/>Surprise
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='spin-btn'>", unsafe_allow_html=True)

    disabled = st.session_state.result_index >= len(SEQUENCE) or st.session_state.spin_animation
    if st.button("🎡 Spin", use_container_width=True, disabled=disabled):
        # next result from sequence
        if st.session_state.result_index < len(SEQUENCE):
            choice = SEQUENCE[st.session_state.result_index]
            st.session_state.result_index += 1

            # map choice to view
            if choice == "Greeting Card":
                st.session_state.card_open = False
                next_view = "greeting"
            elif choice == "Photo Gallery":
                next_view = "gallery"
            elif choice == "Family Wishes":
                next_view = "family"
            elif choice == "Fun Game":
                next_view = "game"
            else:
                next_view = "scratch"

            st.session_state.next_view_after_spin = next_view
            st.session_state.spin_animation = True

            # rerun so upar wala time.sleep wala block execute ho
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def view_greeting():
    st.markdown("<div class='greeting-title'>Greeting Card</div>", unsafe_allow_html=True)

    if not st.session_state.card_open:
        # closed card view
        st.markdown(
            """
            <div class="greeting-card-closed">
                <div style="font-size:60px;margin-bottom:10px;">💘</div>
                <div>Happy 1st Anniversary</div>
                <div style="margin-top:8px;font-size:22px;">Shreyas &amp; Prateeksha</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # open view: left photo, right text
        left, right = st.columns([1, 1.1], gap="large")
        with left:
            st.image(IMAGE_PATH, use_column_width=True)
        with right:
            st.markdown(
                """
                <div class="greeting-text-box">
                    <p><b>To my dearest sister and Jiju,</b></p>
                    <p>
                        Happy Anniversary! It feels like just yesterday I was celebrating your wedding,
                        and now here we are, one year later. You two are a perfect example of true love,
                        and I'm so happy to see you building a beautiful life together, filled with laughter,
                        support, and endless joy.
                    </p>
                    <p>
                        May this first year be the beginning of a lifetime of happiness, and may you both
                        continue to inspire us all with your amazing bond. Here's to many more years of
                        love and adventure!
                    </p>
                    <p style="margin-top:16px; font-style:italic;">
                        With all my love,<br/>
                        Your forever annoying but loving sibling 💖
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
        if st.button("💌 Open Greeting Card" if not st.session_state.card_open else "🔒 Close Greeting Card"):
            st.session_state.card_open = not st.session_state.card_open
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
        if st.button("🎡 Spin Wheel Again"):
            st.session_state.view = "wheel"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def view_gallery():
    play_music(r"C:\Users\WELCOME\Downloads\romantic.mp3")
    st.markdown("<div class='gallery-title'>Photo Gallery 💘</div>", unsafe_allow_html=True)

    IMAGE_FOLDER = r"C:\Users\WELCOME\Downloads\images"
    image_files = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
                   if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        st.warning("No images found in gallery folder.")
        return

    # Slide Index
    if "gallery_index" not in st.session_state:
        st.session_state.gallery_index = 0

    img_path = image_files[st.session_state.gallery_index]
    st.image(img_path, use_container_width=True)

    # Move to next image after 2 sec
    time.sleep(2)
    st.session_state.gallery_index += 1

    # STOP when slideshow ends
    if st.session_state.gallery_index >= len(image_files):
        st.session_state.gallery_index = 0
        st.session_state.view = "wheel"
        st.rerun()

    # AUTOPLAY SLIDESHOW (removes wheel below)
    st.rerun()


def view_family():
    st.markdown("<h1 style='text-align:center; color:white; font-size:50px; font-weight:900;'>Family Wishes ❤️</h1>", unsafe_allow_html=True)
    st.write("")

    # Paths to videos
    video1 = r"C:\Users\WELCOME\Downloads\WhatsApp Video 2025-11-25 at 3.00.31 PM.mp4"
    video2 = r"C:\Users\WELCOME\Downloads\WhatsApp Video 2025-11-25 at 3.09.48 PM.mp4"

    # States to control single play mode
    if "video_playing" not in st.session_state:
        st.session_state.video_playing = None

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<h4 style='text-align:center;color:white;'>Video 1 🎥</h4>", unsafe_allow_html=True)
        if st.button("▶ Play Video 1", key="p1"):
            st.session_state.video_playing = "v1"
            st.rerun()
        if st.button("⏸ Pause 1", key="s1"):
            st.session_state.video_playing = None
            st.rerun()

        if st.session_state.video_playing == "v1":
            st.video(video1, start_time=0)

    with col2:
        st.markdown("<h4 style='text-align:center;color:white;'>Video 2 🎥</h4>", unsafe_allow_html=True)
        if st.button("▶ Play Video 2", key="p2"):
            st.session_state.video_playing = "v2"
            st.rerun()
        if st.button("⏸ Pause 2", key="s2"):
            st.session_state.video_playing = None
            st.rerun()

        if st.session_state.video_playing == "v2":
            st.video(video2, start_time=0)

    st.write("")
    if st.button("⬅ Back to Wheel"):
        st.session_state.view = "wheel"
        st.rerun()


from streamlit.components.v1 import html

from streamlit.components.v1 import html

from streamlit.components.v1 import html

import streamlit.components.v1 as components

import streamlit as st
import streamlit.components.v1 as components
import random

import streamlit as st
import streamlit.components.v1 as components
import json

def view_game():
    st.markdown("<h1 style='text-align:center; color:white; font-size:50px; font-weight:900;'>Guess The Song 🎵 Using Emojis 💖</h1>", unsafe_allow_html=True)
    st.write("")

    quizzes = [
        {"emoji": "👉⚫⚫👀", "answer": "Yeh Kaali Kaali Aankhen"},
        {"emoji": "💧💧🔥", "answer": "Tip Tip Barsa Paani"},
        {"emoji": "😊👩😊", "answer": "Aankh Maare"},
        {"emoji": "👉🥾🇯🇵", "answer": "Mera Jootha Hai Japani"},
        {"emoji": "7 🌊 🏃", "answer": "Saat Samundar Paar"},
        {"emoji": "1 👩‍❤️‍👨 👁 😇", "answer": "Ek Ladki Ko Dekha Toh Aisa Laga"},
        {"emoji": "❤️ ☎️ 🔔", "answer": "Ring Ring Ringa Ringa"},
        {"emoji": "🌞🏙️ + 🌙🔥", "answer": "Suraj Hua Maddham"}
    ]

    if "game_index" not in st.session_state:
        st.session_state.game_index = 0
        st.session_state.game_message = ""
        st.session_state.reveal = False

    index = st.session_state.game_index
    q = quizzes[index]

    st.markdown(f"<h1 style='text-align:center;font-size:70px;'>{q['emoji']}</h1>", unsafe_allow_html=True)

    user_answer = st.text_input("Guess the song name 🎶:", key=f"answer_{index}")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("✔ Check Answer", key=f"check_{index}"):
            if user_answer.strip().lower() == q["answer"].lower():
                st.session_state.game_message = f"🎉 Correct! 🎉 <b>{q['answer']}</b>"
                st.session_state.reveal = True
            else:
                st.session_state.game_message = "❌ Wrong! Try again."
                st.session_state.reveal = True

    with col2:
        if st.button("Show Answer 👀", key=f"reveal_{index}"):
            st.session_state.game_message = f"💡 Correct answer: <b>{q['answer']}</b>"
            st.session_state.reveal = True

    st.markdown(f"<h3 style='text-align:center; color:white;'>{st.session_state.game_message}</h3>", unsafe_allow_html=True)

    st.write("")
    if st.button("➡ Next"):
        if st.session_state.game_index < len(quizzes) - 1:
            st.session_state.game_index += 1
            st.session_state.game_message = ""
            st.session_state.reveal = False
            st.rerun()

    # Display final summary + Back button
    if st.session_state.game_index == len(quizzes) - 1 and st.session_state.reveal:
        st.markdown("<h2 style='text-align:center;color:#ff69b4;'>🎉 You have completed the Game! 🎉</h2>", unsafe_allow_html=True)

        if st.button("🎡 Back to Wheel"):
            st.session_state.game_index = 0
            st.session_state.game_message = ""
            st.session_state.reveal = False
            st.session_state.view = "wheel"
            st.rerun()

def view_scratch():
    st.markdown("<h1 style='text-align:center;font-size:50px;color:white;font-weight:900;'>Scratch & Win Surprise 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;color:white;'>Flip the Coin 🎯</h3>", unsafe_allow_html=True)
    st.write("")

    # Initialize states
    if "coin_flipped" not in st.session_state:
        st.session_state.coin_flipped = False
        st.session_state.coin_result = None

    # CSS for Real Coin Look & Flip Animation
    st.markdown("""
        <style>
        .coin {
            width: 200px;
            height: 200px;
            margin: auto;
            border-radius: 50%;
            background: radial-gradient(circle, #ffd700, #e6b400, #b8860b);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 900;
            color: #7a0033;
            text-shadow: 0 0 10px white;
            box-shadow: 0 0 25px rgba(0,0,0,0.5);
            transform-style: preserve-3d;
        }
        .flip {
            animation: flipCoin 1s ease-out forwards;
        }
        @keyframes flipCoin {
            from { transform: rotateY(0deg); }
            to { transform: rotateY(900deg); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Display Coin
    coin_text = st.session_state.coin_result if st.session_state.coin_flipped else "FLIP ME ❤️"
    animation = "flip" if st.session_state.coin_flipped else ""

    st.markdown(f"""
        <div class="coin {animation}">
            {coin_text}
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Flip button
    if not st.session_state.coin_flipped:
        if st.button("🎯 Flip The Coin 🎯", use_container_width=True):
            st.session_state.coin_flipped = True
            st.session_state.coin_result = random.choice(["🎬 MOVIE DATE ❤️", "🍽 DINNER DATE ❤️"])
            st.rerun()

    # Result + Redeem
    if st.session_state.coin_flipped:
        st.markdown("<h2 style='text-align:center;color:white;font-weight:900;'>🎉 Congratulations 🎉</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;color:#ff007f;font-size:40px;font-weight:900;'>{st.session_state.coin_result}</h2>", unsafe_allow_html=True)
        st.write("")

        if st.button("❤️ Redeem Now ❤️", use_container_width=True):
            st.session_state.view = "redeem"
            st.rerun()

    if st.button("⬅ Back to Wheel"):
        st.session_state.view = "wheel"
        st.rerun()

import streamlit as st
import random
import time

import streamlit as st
import random
import time

import random
import time

import random

def view_coin():
    import time

    st.markdown("<h1 style='text-align:center; color:white; font-size:55px; font-weight:900;'>Flip The Coin 💖</h1>", unsafe_allow_html=True)
    st.write("")

    # Session states setup
    if "coin_flipped" not in st.session_state:
        st.session_state.coin_flipped = False
        st.session_state.coin_result = ""
        st.session_state.show_result = False

    # CSS for coin + flip animation + front/back text correct orientation
    st.markdown("""
        <style>
        .coin {
            width: 200px;
            height: 200px;
            margin: auto;
            border-radius: 50%;
            background: radial-gradient(circle, #fff, #ff9ecb);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 900;
            color: #7a0033;
            box-shadow: 0 0 25px rgba(255,0,90,0.6);
            transform-style: preserve-3d;
            backface-visibility: hidden;
        }
        .flip {
            animation: spinFlip 1s ease-out forwards;
        }
        @keyframes spinFlip {
            0% { transform: rotateY(0deg); }
            100% { transform: rotateY(900deg); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Display Coin
    coin_text = st.session_state.coin_result if st.session_state.show_result else ""

    st.markdown(
        f"""
        <div class="coin {'flip' if st.session_state.coin_flipped and not st.session_state.show_result else ''}">
            {coin_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("\n")

    # Flip button
    if not st.session_state.coin_flipped:
        if st.button("🎯 Flip The Coin 🎯", use_container_width=True):
            st.session_state.coin_flipped = True
            # Generate random result
            st.session_state.coin_result = random.choice(["Lunch Date 💖", "Movie Date 🎬"])
            st.rerun()

    # After flip animation: show result and congratulations
    if st.session_state.coin_flipped and not st.session_state.show_result:
        time.sleep(1.1)  # wait until flip ends
        st.session_state.show_result = True
        st.rerun()

    # Show result only after reveal
    if st.session_state.show_result:
        st.markdown(
            f"<h2 style='text-align:center;color:white;font-weight:900;'>🎉 Congratulations! You Got "
            f"<span style='color:#ff007f;'>{st.session_state.coin_result}</span> 🎉</h2>",
            unsafe_allow_html=True
        )
        st.write("")

        if st.button("❤️ Redeem Now ❤️", use_container_width=True):
            st.session_state.view = "redeem"
            st.session_state.show_result = False
            st.session_state.coin_flipped = False
            st.rerun()

    st.write("")
    if st.button("⬅ Back to Wheel", use_container_width=True):
        st.session_state.coin_flipped = False
        st.session_state.show_result = False
        st.session_state.coin_result = ""
        st.session_state.view = "wheel"
        st.rerun()

def view_redeem():
    st.markdown(
        """
        <div style='text-align:center; background:white; padding:50px; color:#b3004b;
                    border-radius:25px; width:70%; margin:auto; font-size:40px; font-weight:900;
                    box-shadow:0 0 25px rgba(255,0,90,0.5);'>
            Treat for both of you ❤️<br><br>
            Valid anytime, just tell me 😌
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 💮 Petal rain animation
    st.markdown("""
    <style>
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity:1; }
        100% { transform: translateY(120vh) rotate(360deg); opacity:0; }
    }
    .petal {
        position: fixed;
        top: 0;
        font-size: 28px;
        animation: fall linear infinite;
        z-index: 9999;
    }
    </style>
    <script>
    const petalCount = 20;
    for(let i=0; i<petalCount; i++){
        let petal = document.createElement('div');
        petal.className = 'petal';
        petal.innerHTML = '🌹';
        petal.style.left = Math.random() * 100 + 'vw';
        petal.style.animationDuration = (8 + Math.random()*5) + 's';
        document.body.appendChild(petal);
    }
    </script>
    """, unsafe_allow_html=True)




#---------------- ROUTER -----------------
if st.session_state.view == "start":
    view_start()

elif st.session_state.view == "wheel":
    view_wheel()

elif st.session_state.view == "greeting":
    view_greeting()

elif st.session_state.view == "gallery":
    view_gallery()

elif st.session_state.view == "family":
    view_family()

elif st.session_state.view == "game":
    view_game()   # GAME AB YAHAN RENDER HOGA

elif st.session_state.view == "coin":
    view_coin()

elif st.session_state.view == "redeem":
    view_redeem()

elif st.session_state.view == "scratch":
    view_coin()   # scratch replaced with coin

elif st.session_state.view == "final":
    view_final()














