import io
import fluidsynth
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
#audio_data = fluidsynth.raw_audio_string(audio_data)
st.audio(audio_data)
