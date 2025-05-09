# Sketch to Reality
## Transforming Hand-Drawn Design into Multi-modal Immersive Digital Twin

A 2D to 3D pipeline that converts hand‑drawn architectural sketches and user‑defined parameters into immersive panoramas.

---

## Repository Structure

```
project-root/
│
├─ Pen_stroke_app/          # Unified Sketch→CSV→Panorama package
│  ├─ penstroke_app.html        # Sketch UI & CSV export (inputs)
│  ├─ app_output_form/          # Exported CSVs (build.csv, camera.csv)
│  ├─ blender_2D_to_panorama.py # Blender script for geometry & rendering
│  ├─ blender_debug.py          # Debug script for Blender UI
│  ├─ debug.blend               # Blender file for debugging
│  ├─ panorama_input/           # Generated panoramas (outputs)
│  └─ bak_image/                # Background map image
│
└─ UI/                     # Flask & WebXR viewer
   ├─ app.py                    # Flask backend
   ├─ .env.example              # Environment variables template
   ├─ templates/                # HTML templates
   │  └─ index.html             # VR viewer page
   └─ static/                   # Front‑end assets
      ├─ panorama_input/        # Input panoramas to here for display
      ├─ css/                   # Stylesheets
      │  └─ chat.css            # Chat UI styles
      └─ js/                    # JavaScript
         └─ chat.js             # Chat & WebXR logic
```

> **Note:** The first two steps to run have been merged into `Pen_stroke_app/` for a single Sketch-Canvas to Panorama workflow. The `UI/` folder hosts the live demo environment.

> **Note:** Feel free to redirect the output of panorama from `Pen_stroke_app/panorama_input/` to `UI/panorama_input/` for streamlining the process. The current structure was designed for step by step monitoring.

---
## Demo Video

A short demonstration of the Sketch to Reality workflow is available on YouTube:
Follow this link to watch: https://youtu.be/pukzsR8duLI

---

## Prerequisites

* **Python 3.9+**
* **Blender 3.3+** (ensure `blender` is on your PATH)
* A modern web browser (Chrome, Firefox, Safari)

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/YOUR_USERNAME/sketch-to-reality.git
   cd sketch-to-reality
   ```
2. **Install Python dependencies**

   ```bash
   pip install flask python-dotenv openai
   ```
3. **Install Blender**

   * Download from [https://www.blender.org/download/](https://www.blender.org/download/)
   * Verify installation with `blender --version`

---

## Workflow Demo

### 1. Pen\_stroke\_app (2D Sketch → CSV → 3D Model →Panorama)

1. **Open** `Pen_stroke_app/penstroke_app.html` in your browser.
2. **Sketch** footprints, enter building heights, and place position markers.
3. **Export CSVs** into `Pen_stroke_app/app_output_form/`:

   * `build.csv`
   * `camera.csv`
4. **Render Panoramas** by running Blender:

   ```bash
   blender --background --python Pen_stroke_app/blender_2D_to_panorama.py
   ```

   Generated files: `Pen_stroke_app/panorama_input/panorama_*.jpg`

   > **Note:** This is a script that runs the geometry extrusion to renderings. Panorama's render environment & resolution can be further adjusted in the python script.
5. *(Optional)* **Debug** in Blender UI: open `Pen_stroke_app/debug.blend` and run `blender_debug.py` to inspect geometry and camera placements.

### 2. UI (Panorama → Immersive View & Annotations)

1. **Copy** panoramas from `Pen_stroke_app/panorama_input/` into `UI/static/panorama_input/`.
2. **Configure** environment variables:

   ```bash
   cd UI
   cp .env.example .env
   # Edit .env to add your OPENAI_API_KEY
   ```
3. **Launch** the Flask server:

   ```bash
   flask run
   ```
4. **Visit** `http://localhost:5000` to explore VR panoramas, place annotation dots, record audio, and view live transcriptions.

---

## Environment Variables

Copy `.env.example` to `.env` and add your keys:

```ini
OPENAI_API_KEY=your_key_here
```
Here is the instruction to set up your own API on OPEN AI: https://openai.com/index/openai-api/

---

## License

MIT License — see `LICENSE` for details.

---