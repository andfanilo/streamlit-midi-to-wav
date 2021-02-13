import pretty_midi
import soundfile as sf
import streamlit as st

st.title(":tada: Hello world !")

midi_data = pretty_midi.PrettyMIDI('toto-africa.mid')
audio_data = midi_data.fluidsynth()
sf.write('stereo_file.wav', naudio_data, 44100, 'PCM_24')
st.audio('stereo_file.wav')

st.info("End of script, no errors :wink:")
