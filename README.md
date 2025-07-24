# Voice-Controlled Desktop AI Assistant

A smart, voice-controlled desktop assistant built with Python. It can respond to your voice commands, open applications, answer general knowledge questions using AI, fetch time and date, and more — all with hands-free control.

---

## 🔍 Features

- 🎤 **Voice Recognition** using `speech_recognition`
- 🗣️ **Text-to-Speech Output** using `pyttsx3`
- 🧠 **Smart Q&A** powered by [Gemini](https://deepmind.google/technologies/gemini/) (Google's Generative AI)
- 🕒 **Tells current date & time**
- 📂 **Opens desktop apps and files**
- ❌ **Voice-based control to stop responses** (e.g., "ok stop")
- 🌐 Optional: Wikipedia integration (can be replaced with AI)

---

## 🚀 Technologies Used

- Python 3.x
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Google Generative AI API (Gemini)](https://ai.google.dev/)
- `os`, `threading`, `subprocess`, and other standard Python libraries

---

## 🛠️ Installation & Setup

1. **Clone this repo:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**
   - Create a file named `config.py`
   - Add your API key like this:
     ```python
     API_KEY = "your-gemini-api-key"
     ```

4. **Run the assistant:**
   ```bash
   python assistant.py
   ```

---

## 📸 Screenshots or Demo (Optional)

_Add screenshots or demo video links here._

---

## 👨‍💻 Author

**Harrshan S**  
Biomedical Engineering Student @ SRM IST  
Passionate about Artificial Intelligence, Machine Learning, and Innovative Healthcare Solutions.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ✨ Future Plans (Optional)

- Integrate GUI using `tkinter` or `PyQt`
- Add email/SMS functionalities
- Add task reminders and calendar support

---

> _Feel free to fork and customize it for your own use! Contributions welcome._
