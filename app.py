import gradio as gr
import time
import numpy as np
from pathlib import Path

from google import genai
from google.genai import types

from dotenv import load_dotenv
import os
from sarvamai import SarvamAI
from sarvamai.play import save

load_dotenv()
sarvam_key = os.getenv("SARVAM_API_KEY")

google_client = genai.Client()
client = SarvamAI(api_subscription_key=sarvam_key )


if gr.NO_RELOAD:
    stop_generation = None
    prompt = input_file = None

    history = []

    translation = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Bengali": "bn-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN",
        "Kannada": "kn-IN",
        "Malayalam": "ml-IN",
        "Marathi": "mr-IN",
        "Gujarati": "gu-IN",
        "Punjabi": "pa-IN",
        "Odia": "od-IN"
    }

    speakers = {
        "English": ["Mary", "Thoma"],
        "Hindi": ["Divya", "Rohit"],
        "Malayalam": ["Anjali", "Harish"],
        "Tamil": ["Jaya"],
        "Telugu": ["Lalitha", "Prakash"]
    }

    theme = gr.themes.Default(
        text_size=gr.themes.sizes.text_sm,
        font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]
    )

    gr.set_static_paths(paths=[Path.cwd().absolute()/"assets"])


custom_css = """
.gradio-container {
    background: url('/gradio_api/file=assets/landscape.png') no-repeat center center fixed !important;    
    background-size: cover !important;
    background-position: center !important;
}

span.md.svelte-7ddecg.prose> h1, 
span.md.svelte-7ddecg.prose> p,
h2.output-class.svelte-1mutzus {
    color: #ffffff !important;
}


input.svelte-1ae7ssi.svelte-1ae7ssi, textarea.svelte-1ae7ssi.svelte-1ae7ssi{
    background: #000000 !important;
    color: #ffffff !important;

}

div.svelte-1vd8eap {
    border: None !important;
}

div.form.svelte-633qhp,
#color.block.svelte-1svsvh2.auto-margin,
#color.block.svelte-1svsvh2.auto-margin div.wrap-inner.svelte-1hfxrpf,
label.svelte-j0zqjt {    
    border: None !important;
    background-color: #000000 !important;
    color: #ffffff !important;
}


#color.block.svelte-1svsvh2.auto-margin input{
    color: #ffffff !important;
}

#color li {    
    background-color: #000000 !important;
    color: #ffffff !important;
}

#color li:hover {    
    background-color: #ffffff !important;
    color: #000000 !important;
}

    
.center-left-row {
    min-height: 50vh;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;   /* vertical center */
    align-items: flex-start !important;   /* left align */
    padding-left: 1vw;                    /* optional: add some left margin */
}
.center-right-row {
    min-height: 50vh;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;   /* vertical center */
    align-items: flex-end !important;     /* right align */
    margin-left: auto !important;         /* push to right end */
    padding-right: 1vw;                   /* optional: add some right margin */
}
"""

# Generate a 1-second 440 Hz sine wave as a numpy array
sample_rate = 16000
duration = 1  # seconds
frequency = 440  # Hz
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_np = np.array([], dtype=np.int16)  # Initialize audio with empty array


with gr.Blocks(theme=theme, css=custom_css, title="App") as demo:
    gr.Markdown(
    """
    # Night Time Story !!!😴
    Listen to your favorite stories in your language.
    """, elem_id="color")

    with gr.Row():
        with gr.Column(scale=2, min_width=500, elem_classes="center-left-row"):
            lang = gr.Dropdown(
                label="Choose speech language",
                choices=translation.keys(),
                show_label=True,
                interactive=True,
                elem_id="color"
            )

            gr.HTML("</br>")

            chat_input = gr.Textbox(
                interactive=True,
                placeholder="What do you want to listen to?",
                show_label=False,
                submit_btn=True,
                lines=3,
                elem_id="color"
            )

            def story(lang,chat_input):
                translation = {
                    "English": "en-IN",
                    "Hindi": "hi-IN",
                    "Bengali": "bn-IN",
                    "Tamil": "ta-IN",
                    "Telugu": "te-IN",
                    "Kannada": "kn-IN",
                    "Malayalam": "ml-IN",
                    "Marathi": "mr-IN",
                    "Gujarati": "gu-IN",
                    "Punjabi": "pa-IN",
                    "Odia": "od-IN"
                }

                print(lang, chat_input)
                
                response = google_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents="Generate a short bedtime story for children (about 100 words) inspired by Indian culture and tradition. The story should be engaging, positive, and suitable for kids. Write in English."
                )
                
                
                stry = client.text.translate(
                    input=response.text,
                    source_language_code="auto",
                    target_language_code=translation[lang],
                    speaker_gender="Female"
                )

                # Convert text to speech
                audio = client.text_to_speech.convert(
                    target_language_code=translation[lang],
                    text=stry.translated_text,
                    model="bulbul:v2",
                    speaker="arya"
                )
                save(audio, "output.wav")

                return [gr.Label(value=response.text, 
                           show_label=False, 
                           visible=True,
                           elem_id="color"),
                        gr.Audio(value="output.wav", 
                           show_label=True, 
                           visible=True, 
                           show_download_button=False,
                           elem_id="color")]
        
        gr.HTML("</br>")

        with gr.Column(scale=2, min_width=500, elem_classes="center-right-row"):
            out = gr.Label(value="Your story will appear here...", 
                           show_label=False, 
                           visible=True,
                           elem_id="color")
            
            gr.HTML("</br>")
            
            aud = gr.Audio(value=(sample_rate, audio_np), 
                           show_label=True, 
                           visible=True, 
                           show_download_button=False,
                           elem_id="color")
            
            chat_input.submit(story, [lang, chat_input], [out, aud])
        

demo.launch()

