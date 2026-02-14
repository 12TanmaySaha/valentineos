"""
A playful Streamlit app designed to ask someone special to be your Valentine.

This app features a cute loading screen, an interactive question with a “No”
button that dodges clicks, and a heartfelt letter revealed when the user
accepts. The app also uses custom themes defined in `.streamlit/config.toml`.

To run locally, install dependencies with `pip install -r requirements.txt`
and then execute `streamlit run app.py` from within the `valentine_app`
directory.
"""

import random
import time

import streamlit as st


def show_loading_screen() -> None:
    """Display a simple loading screen with a progress bar and an image.

    This function uses a progress bar to simulate loading and displays a
    decorative heart-themed background image. Once loading completes, it
    updates the session state so that the app content will render on the
    next rerun.
    """
    st.image("assets/heart_background.png", use_column_width=True)
    st.write("Loading a little love… 💖")
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.015)
        progress_bar.progress(percent_complete + 1)
    # mark loading as complete and rerun the script
    st.session_state.loading_complete = True
    st.experimental_rerun()


def ask_valentine() -> None:
    """Render the main question asking your Valentine if they'll accept.

    Includes a "Yes" button and a "No" button that moves to a random
    location each time it's clicked. When the user clicks "Yes", the app
    celebrates with balloons and prompts them to open the love letter.
    """
    st.header("Will you be my Valentine? ❤️")
    st.write(
        "I feel like the luckiest person when I'm with you. "
        "On this special day, would you do me the honour of being my Valentine?"
    )
    # Determine the number of columns to create for positioning the buttons.
    num_cols = 6
    columns = st.columns(num_cols)

    # Place the "Yes" button in the first column. When clicked, we mark
    # acceptance and rerun to display the next view.
    if columns[0].button("Yes, of course! 💕", key="yes_button"):
        st.session_state.yes_clicked = True
        # Celebrate with balloons to make the moment feel special.
        st.balloons()
        st.experimental_rerun()

    # Place the "No" button in a column determined by session state. The
    # button's key includes the click count so that Streamlit treats each
    # appearance as a distinct widget and re-renders it correctly.
    no_index = st.session_state.no_position
    # Ensure no_index stays within bounds (avoids index errors on reruns).
    no_index = max(1, min(no_index, num_cols - 1))
    if columns[no_index].button(
        "No 😢", key=f"no_button_{st.session_state.no_clicks}"
    ):
        # Increment click count and move the button to a new random position.
        st.session_state.no_clicks += 1
        st.session_state.no_position = random.randint(1, num_cols - 1)
        st.experimental_rerun()

    # A little encouragement beneath the buttons.
    st.write("I promise to always cherish you! 💖")


def show_letter() -> None:
    """Display a heartfelt letter to your Valentine with decorative images.

    This function uses Streamlit's markdown and image widgets to create a
    romantic letter addressed to "Bucchu". It also triggers a snow effect
    for extra flair.
    """
    st.success("Yay! You said yes! 💕")
    st.write("Thank you for making my day. Here's something special for you:")
    # Prompt to open the letter; once clicked, we reveal the letter content.
    if st.button("Open Love Letter 💌", key="open_letter_button"):
        st.session_state.show_letter = True
        st.experimental_rerun()

    # Only render the letter once the user has chosen to open it.
    if st.session_state.show_letter:
        # Snow effect adds a gentle, celebratory animation over the page.
        st.snow()
        st.markdown(
            "<h2 style='text-align:center;'>Dear Bucchu,</h2>",
            unsafe_allow_html=True,
        )
        st.write(
            """
            From the moment our paths crossed, my world has been brighter and my heart lighter.
            Your smile lights up my day and your kindness warms my soul. On this Valentine's Day,
            I want you to know how much you mean to me. You are my confidant, my best friend,
            and my greatest adventure. Together, we've shared laughter, dreams, and countless
            memories that I will cherish forever.

            Thank you for being you, for all the little things you do, and for the love you share.
            I promise to stand by you, support you, and fill your days with happiness and love.

            Will you please continue this beautiful journey with me?

            With all my love,
            \n[Your Name]
            """
        )
        # Display gallery images to make the letter feel more personal.
        st.image("assets/gallery_heart_1.png", caption="Our hearts hug", use_column_width=True)
        st.image(
            "assets/gallery_heart_2.png",
            caption="Our love circles endlessly",
            use_column_width=True,
        )


def main() -> None:
    """Main entry point for the Streamlit app.

    Handles session state initialization, orchestrates loading, and controls
    navigation between the question and the letter views.
    """
    # Configure the app page. We set the layout and icon here.
    st.set_page_config(
        page_title="Valentine's Day Surprise",
        page_icon="💖",
        layout="centered",
    )

    # Initialize session state variables if they don't exist.
    if "loading_complete" not in st.session_state:
        st.session_state.loading_complete = False
    if "no_position" not in st.session_state:
        st.session_state.no_position = 3
    if "no_clicks" not in st.session_state:
        st.session_state.no_clicks = 0
    if "yes_clicked" not in st.session_state:
        st.session_state.yes_clicked = False
    if "show_letter" not in st.session_state:
        st.session_state.show_letter = False

    # Set a gentle background color using markdown and inline CSS. This
    # targets the body element of the Streamlit app to change the color.
    st.markdown(
        """
        <style>
        body {
            background-color: #FFF5FA;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Show the loading screen on the very first run.
    if not st.session_state.loading_complete:
        show_loading_screen()

    # Decide which part of the app to render based on user interaction.
    if not st.session_state.yes_clicked:
        ask_valentine()
    else:
        show_letter()


if __name__ == "__main__":
    main()