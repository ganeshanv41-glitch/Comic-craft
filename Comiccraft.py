
import os
import gradio as gr
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# 1. Gemini Client Setup
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
client = genai.Client(api_key=API_KEY)


def generate_comic_story(genre, prompt, num_panels):
    """Gemini model-ai payanpadutthi comic script uruvaakkum function."""
    if not prompt.strip():
        return "Thavaru: Dhayaavu seidhu oru kathai karuvai (prompt) உள்ளிடவும்."

    system_instruction = (
        "You are ComicCraft, an expert comic book writer and visual storyteller. "
        "Your task is to take a high-level story concept and generate a structured comic script. "
        "Format the output clearly with: \n"
        "1. Title & Brief Synopsis\n"
        "2. Character Profiles\n"
        "3. Panel-by-Panel breakdown including Visual Description, Dialogue, and Sound Effects (SFX)."
    )

    user_message = f"""
    Comic Genre: {genre}
    Total Panels: {num_panels}
    Story Concept: {prompt}

    Please write a detailed comic script for this concept.
    """

    try:
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


# ---------------------------------------------------------------------------
# 2. Gradio Interface Construction
# ---------------------------------------------------------------------------
custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="purple",
)

with gr.Blocks(theme=custom_theme, title="ComicCraft") as app:
    # Header Banner
    gr.Markdown(
        """
        # 🎨 ComicCraft
        ### *AI-Powered Visual Storytelling & Comic Script Generation*
        ---
        """
    )

    # Main Navigation Tabs
    with gr.Tabs():

        # TAB 1: App Tool / Generator
        with gr.TabItem("🚀 Comic Generator"):
            gr.Markdown("### Generate Panel-by-Panel Comic Scripts")
            with gr.Row():
                with gr.Column(scale=1):
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
                        lines=5,
                        placeholder="Ex: A cybernetic detective solves a mystery in neo-Tokyo...",
                        label="Story Idea / Concept",
                    )
                    generate_btn = gr.Button(
                        "✨ Generate Comic Script", variant="primary"
                    )

                with gr.Column(scale=1):
                    output_story = gr.Textbox(
                        lines=18,
                        label="Generated Script",
                        placeholder="Ungal script inge generate aagum...",
                        interactive=False,
                    )

            generate_btn.click(
                fn=generate_comic_story,
                inputs=[genre_input, prompt_input, panels_input],
                outputs=output_story,
            )

        # TAB 2: Project Overview
        with gr.TabItem("📋 Project Overview"):
            gr.Markdown(
                """
                ## About ComicCraft
                
                **ComicCraft** is an intelligent assistant designed to streamline the storyboarding and script-writing phase for comic creators, graphic novelists, and visual storytellers.

                ### Key Features
                - **Dynamic Panel Breakdown:** Converts simple ideas into panel-by-panel descriptions.
                - **Smart Dialogue & SFX:** Automatically formats speech bubbles, narration captions, and sound effects.
                - **Genre-Adaptive:** Tailors tone and character prompts based on selected genres (Sci-Fi, Superhero, Fantasy, etc.).
                - **Powered by Gemini Models:** Uses cutting-edge LLMs to maintain plot coherence and visual clarity.

                ### Technology Stack
                - **Backend:** Python, Google Gemini API (`gemini-2.5-flash`)
                - **Frontend / UI:** Gradio
                """
            )

        # TAB 3: Team Members
        with gr.TabItem("👥 Team Members"):
            gr.Markdown(
                """
                ## Project Team
                
                | Role | Member Name | Domain / Responsibilities |
                | :--- | :--- | :--- |
                | **Lead Developer** | [Member 1 Name] | AI Integration & API Pipelines |
                | **UI/UX Designer** | [Member 2 Name] | Interface & User Experience Design |
                | **Prompt Engineer** | [Member 3 Name] | Storytelling Logic & System Instructions |
                | **Project Coordinator** | [Member 4 Name] | Documentation & Presentation |
                """
            )

        # TAB 4: Links & Demo
        with gr.TabItem("🔗 Demo & Links"):
            gr.Markdown(
                """
                ## Project Resources & Links

                - **🌐 Live Website / App:** [https://comiccraft.example.com](https://comiccraft.example.com)
                - **🎥 Demo Video (YouTube / Drive):** [Watch Demo Video](https://youtube.com)
                - **💻 GitHub Repository:** [https://github.com/your-repo/comic-craft](https://github.com)
                - **📄 Project Documentation:** [View Documentation](https://example.com/docs)
                """
            )

    # Footer
    gr.Markdown(
        """
        ---
        <center><small>ComicCraft Project © 2026 | Built with Google Gemini API & Gradio</small></center>
        """
    )

# ---------------------------------------------------------------------------
# 3. Launch App
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.launch()
