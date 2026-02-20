# 🌙 Bedtime Story Generator

An AI-powered web-app that generates soothing, culturally-rich bedtime stories and converts them to natural-sounding speech in multiple Indian languages.

## Features

- **Story Generation**: Uses Google's Gemini 2.5 Flash model to create calm, imaginative bedtime stories rooted in Indian culture and traditions
- **Multi-Language Support**: Supports 11 Indian languages:
  - English, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia
- **Text-to-Speech**: Converts stories to natural-sounding audio using Sarvam AI's Bulbul TTS model
- **Cultural Authenticity**: Stories incorporate authentic Indian settings, imagery, and wisdom from traditional tales
- **Interactive Web UI**: Built with Gradio for an intuitive, accessible interface


### Prerequisites

- Python 3.12+
- GPU (recommended for optimal performance; to implement `bedtimestories_github.ipynb` notebook)


The application will launch a local web server. Open your browser and navigate to the provided URL (typically `http://localhost:7860`).

## 📖 How It Works

1. **User Input**: Select your preferred language and describe what kind of story you'd like to hear
2. **Story Generation**: The AI generates an original bedtime story with:
   - Rich Indian cultural settings and imagery
   - Soothing, rhythmic narrative style
   - Calm themes promoting peaceful sleep
3. **Translation**: If a non-English language is selected, the story is translated using Sarvam's translation API
4. **Text-to-Speech**: The story is converted to crisp audio with appropriate pacing and emotion
5. **Output**: Both the story text and audio are displayed side-by-side for your enjoyment



## 📚 Notebooks & Research

The `bedtimestories_github.ipynb` notebook contains the complete development pipeline including:
- Model quantization and optimization
- Story generation with Gemma 2 2B model
- Translation with IndicTrans2
- Text-to-speech synthesis with Parler TTS

This notebook was developed in Google Colab with T4 GPU.

## 🛠️ Technology Stack

- **LLM**: Google Gemini 2.5 Flash (story generation)
- **Translation**: Sarvam AI Translation API (en-IN to Indian languages)
- **Text-to-Speech**: Sarvam AI Bulbul TTS v3
- **Web Framework**: Gradio
- **Language**: Python 3.12

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🌟 Acknowledgments

- Google for the Gemini API
- Sarvam AI for translation and TTS services
- The Gradio team for the web framework
- The open-source communities behind Hugging Face Transformers and related libraries