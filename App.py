import os
import gradio as gr
from google import genai
from google.genai import types

# 1. Gemini Client Setup
# Ungal Gemini API Key-ai inge kodungal (allathu environment variable-il set seyyalaam)
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
client = genai.Client(api_key=API_KEY)


def generate_comic_story(genre, prompt, num_panels):
    """Gemini model-ai payanpadutthi comic script uruvaakkum function."""
    if not prompt.strip():
        return "Thavaru: Dhayaavu seidhu oru kathai karuvai (prompt) உள்ளிடவும்."

    # Model-ukkana system instructions matrum prompt structure
    system_instruction = (
        "You are ComicCraft-AI, an expert comic book writer and visual storyteller. "
        "Your task is to take a high-level story concept and generate a structured comic script. "
        "Format the output clearly with: \n"
        "1. Title & Brief Synopsis\n"
        "2. Character Descriptions\n"
        "3. Panel-by-Panel breakdown including Visual Description, Dialogue, and Sound Effects (SFX)."
    )

    user_message = f"""
    Comic Genre: {genre}
    Total Panels: {num_panels}
    Story Concept: {prompt}

    Please write a detailed comic script for this concept.
    """

    try:
        # Gemini 2.5 Flash model-ai use seydhu text generate seigiroom
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# 2. Gradio Web Interface
with gr.Blocks(title="ComicCraft-AI") as app:
    gr.Markdown("# 🎨 ComicCraft-AI")
    gr.Markdown(
        "**AI Comic Story Creator** - Gemini Model-ai payanpadutthi ungal comic kathaiyai panel-by-panel script-aaga maatrungal!"
    )

    with gr.Row():
        with gr.Column():
            genre_input = gr.Dropdown(
                choices=[
                    "Superhero",
                    "Sci-Fi",
                    "Fantasy",
                    "Horror",
                    "Humor",
                    "Slice of Life",
                ],
                value="Superhero",
                label="Comic Genre",
            )
            panels_input = gr.Slider(
                minimum=3,
                maximum=8,
                value=4,
                step=1,
                label="Number of Panels",
            )
            prompt_input = gr.Textbox(
                lines=4,
                placeholder="Ex: A young programmer discovers their keyboard can control real-world gravity...",
                label="Story Idea / Concept",
            )
            generate_btn = gr.Button("🚀 Generate Comic Script", variant="primary")

        with gr.Column():
            output_story = gr.Textbox(
                lines=18,
                label="Generated Comic Script",
                interactive=False,
            )

    generate_btn.click(
        fn=generate_comic_story,
        inputs=[genre_input, prompt_input, panels_input],
        outputs=output_story,
    )

# 3. App Launch
if __name__ == "__main__":
    app.launch()
