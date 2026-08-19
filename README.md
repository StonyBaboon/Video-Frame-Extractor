# 🎞️ Video Frame Extractor

A simple and lightweight Python application for extracting frames from videos at configurable time intervals.

The application provides a graphical interface where you can select a video, choose where to save the extracted images, define the extraction interval, and choose how frames are selected.

## ✨ Features

* 🎥 Select videos directly from a graphical interface
* 📁 Choose the output folder
* ⏱️ Configure the extraction interval
* 🎲 Select a random frame from each interval
* 🎯 Select a specific frame from each interval
* 🔢 Extract all intervals or define a custom number of frames
* 📊 Display video information:

  * FPS
  * Total frames
  * Resolution
  * Duration
* 📈 Extraction progress bar
* ⏹️ Stop extraction at any time
* 🌍 Multi-language interface
* 🇵🇹 Portuguese
* 🇬🇧 English
* 🧩 Easy to add additional languages
* 🖼️ Saves extracted frames as JPG images

---

## 🧠 How It Works

The application divides the video into time intervals.

For example, if you configure:

```text
Interval: 2 seconds
```

a video is divided into:

```text
0 ───── 2s ───── 4s ───── 6s ───── 8s ───── ...
```

The application then selects one frame from each interval.

### 🎲 Random Frame

With **Random Frame** selected, the application randomly chooses one frame from every interval.

For example:

```text
0–2s   → random frame
2–4s   → random frame
4–6s   → random frame
6–8s   → random frame
```

The frame is selected independently for each interval.

---

### 🎯 Specific Frame

With **Specific Frame** selected, you can specify which frame should be selected relative to the beginning of each interval.

For example:

```text
Interval: 2 seconds
Specific frame: 30
```

If the video has 60 FPS:

```text
0–2s   → frame 30
2–4s   → frame 30
4–6s   → frame 30
6–8s   → frame 30
```

The frame number is relative to each interval, rather than being an absolute frame number from the beginning of the video.

---

## 🖼️ Output

Extracted images are saved sequentially:

```text
frame_000001.jpg
frame_000002.jpg
frame_000003.jpg
frame_000004.jpg
...
```

The images are saved with high JPEG quality.

---

## 📂 Project Structure

```text
VideoFrameExtractor/
│
├── main.py
│
├── languages/
│   ├── pt.json
│   └── en.json
│
└── README.md
```

### `main.py`

Contains the main application, graphical interface and video-processing logic.

### `languages/`

Contains the translation files used by the application.

Each language is stored in its own JSON file.

---

## 🌍 Adding a New Language

The application is designed to make adding languages easy.

To add a new language, create another JSON file inside:

```text
languages/
```

For example:

```text
languages/
├── pt.json
├── en.json
└── es.json
```

The new file should contain the same translation keys as the existing language files.

For example:

```json
{
    "_language_name": "Español",
    "app_title": "Extractor de Frames de Vídeo",
    "language": "Idioma",
    "video": "Vídeo"
}
```

The application automatically scans the `languages` folder and loads the available language files.

This means additional languages can be added without modifying the main Python code.

---

## 🛠️ Requirements

* Python 3.9 or newer
* OpenCV
* Tkinter

OpenCV can be installed with:

```bash
pip install opencv-python
```

Tkinter is included with most standard Python installations on Windows.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/StonyBaboon/Video-Frame-Extractor.git
```

Enter the project directory:

```bash
cd VideoFrameExtractor
```

Install the dependency:

```bash
pip install opencv-python
```

Run the application:

```bash
python main.py
```

---

## 🖥️ Usage

1. Start the application.
2. Select the video you want to process.
3. Select the destination folder.
4. Choose the extraction interval.
5. Select one of the extraction modes:

   * **Random Frame**
   * **Specific Frame**
6. Choose whether to process all intervals or a specific number.
7. Click **EXTRACT FRAMES**.
8. Wait for the extraction to finish.

The extracted images will appear in the selected output folder.

---

## 📌 Example

Suppose you have a 10-minute video at 60 FPS.

You configure:

```text
Interval: 2 seconds
Mode: Random Frame
Quantity: All
```

The application will process approximately:

```text
600 / 2 = 300 intervals
```

and produce approximately:

```text
300 images
```

with one randomly selected frame from each 2-second interval.

---

## 🔧 Technologies

This project currently uses:

* **Python** — Application logic
* **Tkinter** — Graphical user interface
* **OpenCV** — Video processing and frame extraction
* **JSON** — Language/translation files
* **Threading** — Keeps the GUI responsive during extraction

---

## 📈 Future Improvements

Possible future features include:

* [ ] PNG output
* [ ] JPEG quality control
* [ ] Multiple frames per interval
* [ ] Preview selected frames
* [ ] Video timeline preview
* [ ] Drag & drop video support
* [ ] Dark mode
* [ ] More languages
* [ ] Custom output filename patterns
* [ ] Automatic dataset organization
* [ ] Image metadata
* [ ] Hardware-accelerated video processing

---

## 🤝 Contributing

Contributions are welcome.

If you want to add a new language, improve the interface, fix a bug, or add a feature, feel free to open a Pull Request.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
