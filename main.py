import webbrowser
from random import choice

import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
import time
import vosk
import sys
import sounddevice as sd
import queue
import json

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""
def random_how_are_you_response():
    responses = [
        "Всё отлично, спасибо!",
        "Неплохо, как у вас?",
        "У меня всё хорошо!",
        "Отлично, спрашивайте, чем могу помочь."
    ]
    return choice(responses)
def random_greeting_response():

    responses = [
        "Привет!",
        "Здравствуй!",
        "Доброго времени суток!",
        "Приветствую вас!",
        "Здравствуйте!"
    ]
    return choice(responses)
def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")
    assistant.recognition_language = "ru-RU"
    ttsEngine.setProperty("voice", voices[0].id)


def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def search_in_browser(query):
    if 'найди' in query:
        browser_index = query.index('найди') if 'найди' in query else -1
    elif 'открой' in query:
        browser_index = query.index('открой') if 'открой' in query else -1
    elif 'браузере' in query:
        browser_index = query.index('браузере') if 'браузере' in query else -1
    if browser_index != -1 and browser_index + 1 < len(query):
        string = ' '.join(query[browser_index + 1:])

    search_url = f'https://yandex.ru/search/?text={string}'
    webbrowser.open(search_url)
    play_voice_assistant_speech('Вот что я смог найти по этому зопросу в яндекс')
def greeting():
    response = random_greeting_response()
    play_voice_assistant_speech(response)
def praise_response():
    responses = [
        "Спасибо, рад был помочь!",
        "Благодарю вас!",
        "Спасибо за добрые слова!",
        "Очень приятно, спасибо!",
        "Спасибо большое!"
    ]
    return choice(responses)

def razbor_comard(query):
    for k, v in commands_dict['commands'].items():
        if any(keyword in query for keyword in v):
            handle_command(k, query)
            break


def handle_command(command_key, query=None):
    if command_key == 'greeting':
        greeting()
    elif command_key == 'introduce':
        play_voice_assistant_speech("Я ваш голосовой ассистент Гога."
                                    "Я могу помочь вам с различными задачами, которые связанны с управлением компьютера. "
                                    "Просто попраси меня, и я постараюсь помочь.")
    elif command_key == 'create':
        play_voice_assistant_speech("Меня создал лутший программист - Серафим.")
    elif command_key == 'search':
        search_in_browser(query)
    elif command_key == 'goodbye':
        play_voice_assistant_speech("До свидания! Я завершаю свою работу.")
        exit()
    elif command_key == 'praise':
        response = praise_response()
        play_voice_assistant_speech(response)
    elif command_key == 'how_are_you':
        response = random_how_are_you_response()
        play_voice_assistant_speech(response)
    else:
        play_voice_assistant_speech("Извините, я не понял команду")


def record_and_recognize_audio(*args: tuple):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                return (json.loads(rec.Result())["text"])
    # with microphone:
    #     recognized_data = ""
    #     recognizer.adjust_for_ambient_noise(microphone, duration=0.6)
    #     try:
    #         print("Слушаю, вас")
    #         audio = recognizer.listen(microphone, 5, 5)
    #     except speech_recognition.WaitTimeoutError:
    #         play_voice_assistant_speech("Проверь совой микрофон пожалуйста!")
    #         return
    #     try:
    #         print("Распознание")
    #         recognized_data = recognizer.recognize_google(audio, language="ru").lower()
    #
    #     except speech_recognition.UnknownValueError:
    #         pass
    #
    #     except speech_recognition.RequestError:
    #         play_voice_assistant_speech("Проверь свой интернет!")
    #     return recognized_data
def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

if __name__ == "__main__":
    commands_dict = {
        'commands': {
            'greeting': ['привет', 'здравствуй', 'здравствуйте','добрый', 'день', 'вечер', 'утро','приветствую', 'здравствуйте', 'приветствую вас','приветик', 'здорово', 'хай'],
            'introduce': ['расскажи', 'о себе'],
            'create': ['создал', 'автор', 'кто'],
            'goodbye': ['пока', 'до свидания', 'до встречи', 'прощай', 'заверши работу'],
            'search': ['найди','браузер','открой', 'интернете'],
            'praise': ['спасибо','благодарю','молодец', 'хороший'],
            'how_are_you': ['как',  'дела', 'как', 'ты']
        }
    }

    model = vosk.Model("model")
    samplerate = 16000
    device = 1
    q = queue.Queue()

    ttsEngine = pyttsx3.init()
    assistant = VoiceAssistant()
    assistant.name = "Goga"
    assistant.sex = "male"
    assistant.speech_language = "ru"
    setup_assistant_voice()
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    while True:
        voice_input = record_and_recognize_audio()
        print(voice_input)
        if voice_input == None:
            play_voice_assistant_speech("Извините, я не понял команду")
        voice_input = voice_input.split(" ")
        razbor_comard(voice_input)