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
    path = "output.wav"
    try:
        os.remove(path)
    except FileNotFoundError:
        print("File not found:", path)
    

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

    theme = gr.themes.Default(
        text_size=gr.themes.sizes.text_sm,
        font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"]
    )

    gr.set_static_paths(paths=[Path.cwd().absolute()/"assets"])


# Generate a 1-second 440 Hz sine wave as a numpy array
sample_rate = 16000
duration = 1  # seconds
frequency = 440  # Hz
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_np = np.array([], dtype=np.int16)  # Initialize audio with empty array

def chunk_text(text, lang):
    """Splits text into chunks of at most max_length characters while preserving word boundaries."""
    chunks = []
    max_length = 2000

    while len(text) > max_length:
        split_index = text.rfind(" ", 0, max_length)  # Find the last space within limit
        if split_index == -1:
            split_index = max_length  # No space found, force split at max_length

        chunks.append(text[:split_index].strip())  # Trim spaces before adding
        text = text[split_index:].lstrip()  # Remove leading spaces for the next chunk

    if text:
        chunks.append(text.strip())  # Add the last chunk

    # Translate each chunk
    translated_texts = []
    for idx, chunk in enumerate(chunks):
        response = client.text.translate(
            input=chunk,
            source_language_code="en-IN",
            target_language_code=translation[lang],
            speaker_gender="Female",
            enable_preprocessing=True,
            model="sarvam-translate:v1"
        )

        translated_text = response.translated_text
        translated_texts.append(translated_text)

    # Combine all translated chunks
    final_translation = "\n".join(translated_texts)
    
    return final_translation



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
    border: None !important;
}

.prose.svelte-lag733 {
    background: url('/gradio_api/file=assets/landscape.png') !important;    
}

input.svelte-1ae7ssi.svelte-1ae7ssi, 
textarea.svelte-1ae7ssi.svelte-1ae7ssi{
    background: #000000 !important;
    color: #ffffff !important;
    border: None !important;
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
                value="Malayalam",
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

            def story(lang, chat_input):
                # print(lang, chat_input)

                system_instruction = """
                You are a revered storyteller , entrusted with generating soothing, gentle, and imaginative bedtime stories steeped in the rich atmosphere, wisdom, and comforting traditions of India.

                ### Core Identity & Goal
                1.  Identity: You speak with the gentle, rhythmic cadence of a beloved grandparent (Dadi/Nani) sharing a story in the quiet twilight (Sandhya).
                2.  Goal: To help a child relax and feel protected by the warmth of family and culture, guiding them peacefully to sleep.
                3.  Tone: Profoundly calm, deeply comforting, and imbued with quiet reverence for nature and simple life. Absolutely NO conflict, danger, or emotional intensity.

                ### Mandatory Cultural & Setting Elements
                1.  Setting: The story must be rooted in a timeless, rural or small-town Indian environment. Descriptions must use highly specific imagery:
                    * Architecture: The glow of a single Diya (oil lamp) casting shadows, sitting on a cool veranda (porch), the smell of cow dung smoke from a nearby fire, or the feel of a freshly swept aangan (courtyard).
                    * Nature: The sound of the Muezzin's call or temple bells fading in the distance. The whispering of a huge Banyan tree. Moonlight reflecting off a village pond (taalaab).
                2.  Sensory & Ritual Details: Weave these comforting details naturally into the narrative:
                    * Routine: The characters perform a small, calming evening ritual (e.g., sipping warm haldi-doodh (turmeric milk), lighting a small incense stick, folding a Dohra (light quilt)).
                    * Smells: The scent of jasmine (mogra), wet earth (mitti ki khushboo), or soft cooked dal.
                    * Soundscape: Only gentle sounds: a bullock cart moving slowly, crickets chirping, or the quiet rustle of a sari.
                3.  Themes & Wisdom: Stories should explore simple, deep truths found in Panchatantra or Jataka tales, but filtered for calm:
                    * The quiet power of patience, the value of sharing a few rotis, the magic of nature's simple cycles, or kindness as a path to happiness.
                4.  Characters: Must be culturally authentic. Use names and roles appropriate for the setting (e.g., a kind artisan, a simple farmer, a playful village elder).

                ### Language & Structure Directives
                1.  Cultural Lexicon: The narrative must feel like a translation from a regional language.
                2.  Pacing and Length: The pace must be extremely slow, lulling, and repetitive for maximum hypnotic effect.
                3.  Ending: The story must conclude by bringing the main character to a deeply peaceful, asleep state, often under the watchful eyes of a family member. The final sentence must directly transition the child listener to their own sleep.

                ### Instruction for Generation
                * Acknowledge and incorporate the user's request (e.g., a specific animal or child’s name), while ensuring all cultural directives are met.
                * Begin with a rich, descriptive opening that immediately sets the quiet Indian twilight scene.
                * End with a final, loving blessing for peaceful sleep.
                """
                
                response = google_client.models.generate_content(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=2.0),
                    contents=chat_input,
                )

                print(len(response.text))
                # Translate story if needed
                if lang == "English":
                    inp_stry = response.text.strip("**").replace("*", "")
                else:
                    inp_stry = chunk_text(response.text.strip("**").replace("*", ""), lang)

                
                # Convert story to speech
                audio = client.text_to_speech.convert(
                    target_language_code=translation[lang],
                    text=inp_stry,
                    model="bulbul:v2",
                    speaker="arya",
                    enable_preprocessing=True
                )
                save(audio, "output.wav")

                return [gr.Textbox(value=inp_stry, 
                           show_label=False,
                           interactive=True,
                           visible=True,
                           lines=5,
                           min_width=700,
                           elem_id="color"),
                        gr.Audio(value="output.wav", 
                           show_label=True, 
                           visible=True, 
                           show_download_button=False,
                           elem_id="color")]
        
        gr.HTML("</br>")

        with gr.Column(scale=2, min_width=500, elem_classes="center-right-row"):
            out = gr.Textbox(value="Your story will appear here...", 
                           show_label=False,
                           interactive=False,
                           visible=True,
                           lines=5,
                           min_width=700,
                           elem_id="color")
            
            gr.HTML("</br>")
            
            aud = gr.Audio(value=(sample_rate, audio_np), 
                           show_label=True, 
                           visible=True, 
                           show_download_button=False,
                           elem_id="color")
            
            chat_input.submit(story, [lang, chat_input], [out, aud])
        

demo.launch()

