import pretty_midi
import streamlit as st

st.title(":tada: Hello world !")

midi_data = pretty_midi.PrettyMIDI('toto-africa.mid')
audio_data = midi_data.synthesize()
st.audio(audio_data)

st.info("End of script, no errors :wink:")
