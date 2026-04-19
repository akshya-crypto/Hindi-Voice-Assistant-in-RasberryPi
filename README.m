# Raspberry Pi Offline Voice Assistant

## Overview
An offline voice assistant built on Raspberry Pi that performs speech recognition and text-to-speech without internet access.

---

## Features
- Offline speech recognition (Vosk)  
- Text-to-speech output (eSpeak)  
- Lightweight and efficient  
- Works without internet  

---

## Tech Stack
- Python 3  
- Vosk  
- eSpeak  
- SoundDevice / ALSA  

---

## Installation
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-pip espeak
pip3 install vosk sounddevice