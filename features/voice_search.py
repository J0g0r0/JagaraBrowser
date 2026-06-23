import speech_recognition as sr

def voice_search(window):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        window.statusBar().showMessage("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="id-ID")
        window.current_tab().navigate(f"https://www.google.com/search?q={text}")
    except:
        window.statusBar().showMessage("Voice not recognized")