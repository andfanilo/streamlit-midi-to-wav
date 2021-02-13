import io
import numpy as np
import pretty_midi
from scipy.io import wavfile
import streamlit as st

st.title(":tada: Convert a MIDI file to Sound")

uploaded_file = st.file_uploader("Upload MIDI file", type=["mid"])

if uploaded_file is None:
  st.info("Please upload a MIDI file")
  st.stop() 

midi_data = pretty_midi.PrettyMIDI(uploaded_file)
audio_data = midi_data.fluidsynth()

virtualfile = io.BytesIO()
wavfile.write(virtualfile, 44100, audio_data.astype(np.int16))

st.audio(virtualfile)
