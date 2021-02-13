import pretty_midi
import soundfile as sf
import streamlit as st

st.title(":tada: Convert a MIDI file to Sound")

uploaded_file = st.file_uploader("Upload MIDI file", type=["mid"])

if uploaded_file is None:
  st.info("Please upload a MIDI file")
  st.stop() 

midi_data = pretty_midi.PrettyMIDI(uploaded_file)
audio_data = midi_data.fluidsynth()
sf.write('stereo_file.wav', audio_data, 44100, 'PCM_24')
st.audio('stereo_file.wav')
