import gradio as gr
import time
import numpy as np
from pathlib import Path
from google import genai
from google.genai import types


if gr.NO_RELOAD:
    stop_generation = None
    prompt = input_file = None

    history = []

    translation = {
        "English": "eng_Latn",
        "Hindi": "hin_Deva",
        "Malayalam": "mal_Mlym",
        "Tamil": "tam_Taml",
        "Telugu": "tel_Telu"
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

client = genai.Client()

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

            def story():
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents="How does AI work?"
                )
                print(response.text)

                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents="Say cheerfully: Have a wonderful day!",
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='Kore',
                                )
                            )
                        ),
                    )
                )

                data = response.candidates[0].content.parts[0].inline_data.data
                file_name='out.wav'



            chat_input.submit(story, None, None)
        
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

demo.launch()

