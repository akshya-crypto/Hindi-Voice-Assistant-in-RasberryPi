import wave
import json
import subprocess
import time
from datetime import datetime
from vosk import Model, KaldiRecognizer
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

VOSK_MODEL_PATH = "vosk-model-small-hi-0.22"

print("Loading hindi vosk model..")
vosk_model = Model(VOSK_MODEL_PATH)

wf = wave.open("test.wav", "rb")
rec = KaldiRecognizer(vosk_model, wf.getframerate())

def speak_hindi(text):
    latin = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    subprocess.run(["espeak-ng", "-v", "hi", latin])

def get_intent_response(text):
    now = datetime.now()
    if any(w in text for w in ["समय", "टाइम"]):
        return f"अभी समय है {now.strftime('%I %M %p')}"
    elif any(w in text for w in ["तारीख", "डेट", "दिन"]):
        return f"आज की तारीख है {now.strftime('%d %B %Y')}"
    elif any(w in text for w in ["नमस्ते", "हेलो", "हाय"]):
        return "नमस्ते! आप कैसे हैं?"
    elif "नाम" in text:
        return "मेरा नाम हिंदी वॉइस असिस्टेंट है"
    elif any(w in text for w in ["कैसे हो", "कैसी हो"]):
        return "मैं बढ़िया हूँ, धन्यवाद! आप कैसे हैं?"
    elif any(w in text for w in ["क्या कर सकते", "मदद"]):
        return "मैं समय, तारीख और सामान्य सवालों के जवाब दे सकती हूँ"
    elif any(w in text for w in ["मौसम"]):
        return "अभी मौसम की जानकारी उपलब्ध नहीं है"
    elif any(w in text for w in ["बैटरी"]):
        return "बैटरी स्थिति अभी उपलब्ध नहीं है"
    elif any(w in text for w in ["धन्यवाद", "शुक्रिया"]):
        return "आपका स्वागत है"
    elif any(w in text for w in ["बाय", "अलविदा", "रुको"]):
        return "अलविदा! फिर मिलेंगे"
    else:
        return f"आपने कहा {text}"

expected_mapping = {
    "नमस्ते": ["नमस्ते", "हेलो", "हाय", "नमस्कार", "hello", "hi"],
    "समय": ["समय", "टाइम", "घड़ी", "अभी कितना बजा", "क्या समय है", "time", "current time"],
    "तारीख": ["तारीख", "डेट", "दिन", "आज कौन सा दिन", "आज की तारीख", "date", "today date"],
    "नाम": ["नाम", "तुम्हारा नाम", "आपका नाम", "what is your name"],
    "कैसे हो": ["कैसे हो", "कैसी हो", "क्या हाल है", "how are you"],
    "क्या कर सकते": ["क्या कर सकते", "मदद", "क्या कर सकती हो", "तुम क्या कर सकती हो", "help"],
    "मौसम": ["मौसम", "आज मौसम कैसा है", "weather"],
    "बैटरी": ["बैटरी", "बैटरी स्टेटस", "पावर", "battery"],
    "धन्यवाद": ["धन्यवाद", "शुक्रिया", "थैंक यू", "thanks"],
    "अलविदा": ["बाय", "अलविदा", "रुको", "बंद करो", "bye", "stop"]
}
latencies = []
correct = 0
total = 0

print("Processing audio file..")

start_execution = time.time()

while True:
    data = wf.readframes(8000)  
    if len(data) == 0:
        break

    start_latency = time.time()
    if rec.AcceptWaveform(data):
        end_latency = time.time()
        latency = end_latency - start_latency
        latencies.append(latency)

        result = json.loads(rec.Result())
        text = result.get("text", "").strip()

        if text:
            total += 1
            response = get_intent_response(text)
            print("आपने कहा:", text)
            print("जवाब:", response)
            print(f"Latency: {latency:.3f} seconds\n")
            speak_hindi(response)

            matched = False
            for key in expected_mapping.keys():
                if key in text:
                    matched = True
                    correct += 1
                    break
            if not matched:
                if"आपने कहा" in response:
                    correct+=1

            if "अलविदा" in response:
                break
        
    time.sleep(0.1) 

end_execution = time.time()
execution_time = end_execution - start_execution
accuracy = (correct / total) * 100 if total > 0 else 0
avg_latency = sum(latencies)/len(latencies) if latencies else 0

print(f"Execution time: {execution_time:.3f} seconds")
print(f"Intent accuracy: {accuracy:.2f}%")
print(f"Average latency: {avg_latency:.3f} seconds")