import io

import numpy as np
import pretty_midi
import requests
import streamlit as st
from bs4 import BeautifulSoup
from scipy.io import wavfile


@st.cache(allow_output_mutation=True)
def load_session():
    return requests.Session()


def has_download_attr(tag):
    return tag.has_attr("download")


@st.cache(hash_funcs={requests.Session: id}, allow_output_mutation=True)
def download_from_bitmidi(url: str, sess: requests.Session) -> bytes:
    user_agent = {"User-agent": "bot"}
    r_page = sess.get(url, headers=user_agent)
    soup = BeautifulSoup(r_page.content, "html.parser")
    link = soup.find(lambda tag: tag.name == "a" and tag.has_attr("download"))
    if link is None:
        st.error(f"No MIDI file found on page '{url}'")
        raise ValueError(f"No MIDI file found on page '{url}'")

    url_midi_file = "https://bitmidi.com" + link["href"]
    r_midi_file = sess.get(url_midi_file, headers=user_agent)
    return r_midi_file.content


def main():
    st.title(":musical_note: Convert a MIDI file to WAV")
    sess = load_session()

    uploaded_file = st.file_uploader("Upload MIDI file", type=["mid"])
    bitmidi_link = st.text_input(
        "Or input BitMidi URL", "https://bitmidi.com/queen-bohemian-rhapsody-mid"
    )

    midi_file = None

    if uploaded_file is None:
        if "https://bitmidi.com/" not in bitmidi_link:
            st.error("Make sure your URL is of type 'https://bitmidi.com/<midi_name>'")
            st.stop()
        with st.spinner(f"Downloading MIDI file from {bitmidi_link}"):
            midi_file = io.BytesIO(download_from_bitmidi(bitmidi_link, sess))
    else:
        midi_file = uploaded_file

    st.markdown("---")

    with st.spinner(f"Transcribing to FluidSynth"):
        midi_data = pretty_midi.PrettyMIDI(midi_file)
        audio_data = midi_data.fluidsynth()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)

    st.audio(virtualfile)
    st.markdown("Download the audio by right-clicking on the media player")


if __name__ == "__main__":
    st.set_page_config(
        page_title="MIDI to WAV",
        page_icon="musical_note",
        initial_sidebar_state="collapsed",
    )
    main()
    with st.sidebar:
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@andfanilo</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin: 0.75em 0;"><a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )
