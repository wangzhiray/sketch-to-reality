````markdown
# Sketch to Reality

A web-based 2D→3D pipeline that converts hand-drawn architectural sketches and user-defined parameters into immersive VR panoramas.

---

## Repository Structure

```plaintext
project-root/
├─ package1_sketch_to_csv/
│  └─ penstroke_app.html
├─ package2_csv_to_panorama/
│  ├─ blender_2D_to_panorama.py
│  ├─ blender_debug.py
│  └─ debug.blend
└─ package3_vr_ui/
   ├─ app.py
   ├─ .env.example
   ├─ templates/
   │  └─ index.html
   └─ static/
      ├─ css/
      │  └─ chat.css
      └─ js/
         └─ chat.js
````

---

## Prerequisites

* **Python 3.9+**
* **Blender 3.3+** (make sure `blender` is on your `$PATH`)
* A modern web browser (Chrome, Firefox, Safari)

---

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/YOUR_USERNAME/sketch-to-reality.git
   cd sketch-to-reality
   ```

2. **Install Python deps**

   ```bash
   pip install flask python-dotenv openai
   ```

3. **Install Blender**

   * Download from [https://www.blender.org/download/](https://www.blender.org/download/)
   * Ensure you can run `blender --version` in your terminal.

---

## Demo Workflow

### 1. Sketch → CSV (package1\_sketch\_to\_csv)

1. Open `penstroke_app.html` in your browser
2. Draw footprints, camera markers & heights
3. Export `build.csv` and `camera.csv`
4. Move them into `package2_csv_to_panorama/app_output_form/`

### 2. CSV → Panorama (package2\_csv\_to\_panorama)

1. Confirm CSVs in `app_output_form/`
2. Run:

   ```bash
   blender --background --python blender_2D_to_panorama.py
   ```
3. *(Optional)* Debug in Blender: open `debug.blend` and run `blender_debug.py`
4. Move generated `panorama_*.jpg` into `package3_vr_ui/static/panorama_input/`

### 3. Panorama → VR UI (package3\_vr\_ui)

1. Copy panoramas to `static/panorama_input/`
2. In `package3_vr_ui/`:

   ```bash
   cp .env.example .env
   # edit .env to add your OPENAI_API_KEY
   ```
3. Start server:

   ```bash
   flask run
   ```
4. Visit `http://localhost:5000` to explore & annotate

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your keys.

---

## .gitignore & .env.example

* Use a Python `.gitignore` (ignores `__pycache__/`, `.env`, etc.).
* `.env.example` lists required vars without secrets.

---

## License

MIT License – see `LICENSE` for details.

```

After saving that as **README.md**, open the file in your editor’s Markdown preview (or push it and view it on GitHub.com) to confirm the headings and code block render as expected.
```
