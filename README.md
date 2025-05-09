Sketch to Reality

A web-based 2D to 3D pipeline that converts hand‑drawn architectural sketches and user‑defined parameters into immersive VR panoramas.

Repository Structure

project-root/
├── package1_sketch_to_csv/        # HTML sketch app → CSV export
│   └── penstroke_app.html
├── package2_csv_to_panorama/      # Blender scripts → panorama rendering
│   ├── blender_2D_to_panorama.py
│   ├── blender_debug.py
│   └── debug.blend
├── package3_vr_ui/                # Flask app + WebXR viewer
    ├── app.py
    ├── .env.example
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/chat.css
        └── js/chat.js

Note: Folders are separated for debugging; you can merge them into a single streamlined structure in production.

Prerequisites

Python 3.9+

Blender 3.3+ (add blender to your PATH)

A modern web browser (Chrome, Firefox, Safari)

Installation

Clone the repository

git clone https://github.com/YOUR_USERNAME/sketch-to-reality.git
cd sketch-to-reality

Install Python dependencies

pip install flask python-dotenv openai

Install Blender

Download from https://www.blender.org/download/

Ensure the blender command is available in your terminal.

Demo Workflow

1. Sketch → CSV (package1_sketch_to_csv)

Open penstroke_app.html in your browser.

Draw footprints, place camera markers, and label heights.

Click the download button to export build.csv and camera.csv.

Move these CSVs into package2_csv_to_panorama/app_output_form/.

2. CSV → Panorama (package2_csv_to_panorama)

Verify build.csv and camera.csv are in app_output_form/.

Run Blender in background:

blender --background --python blender_2D_to_panorama.py

This generates panorama_*.jpg in package2_csv_to_panorama/panorama_input/.

(Optional) Debug in Blender UI:

Open debug.blend and run blender_debug.py in the Text Editor.

Move rendered panoramas into package3_vr_ui/static/panorama_input/.

3. Panorama → VR UI (package3_vr_ui)

Copy panorama_*.jpg files into static/panorama_input/.

Create .env from .env.example:

cd package3_vr_ui
cp .env.example .env
# Edit .env to add your OPENAI_API_KEY

Launch the Flask server:

flask run

Visit http://localhost:5000 to explore panoramas, annotate, and transcribe audio.

Environment Variables

Copy .env.example to .env and fill in your API keys.

.gitignore & .env.example

A Python .gitignore excludes __pycache__, .env, and other artifacts.

.env.example lists required variables without secrets.

