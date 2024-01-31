import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
import time

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")
    assistant.recognition_language = "ru-RU"
    ttsEngine.setProperty("voice", voices[0].id)


def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def greeting():
    play_voice_assistant_speech("Привет, меня зовут Гога! Я готов помочь тебе помочь вам с различными задачами.!")


def razbor_comard(query):
    for k, v in commands_dict['commands'].items():
        if any(keyword in query for keyword in v):
            handle_command(k)
            break


def handle_command(command_key):
    if command_key == 'greeting':
        greeting()
    elif command_key == 'introduce':
        play_voice_assistant_speech("Привет, я ваш голосовой ассистент Гога. Меня создал Серафим. "
                                    "Я могу помочь вам с различными задачами, которые связанны с управлением компьютера. "
                                    "Просто попраси меня, и я постараюсь помочь.")


def record_and_recognize_audio(*args: tuple):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=0.6)
        try:
            print("Слушаю, вас")
            audio = recognizer.listen(microphone, 5, 5)
        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech("Проверь совой микрофон пожалуйста!")
            return
        try:
            print("Распознание")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        except speech_recognition.RequestError:
            play_voice_assistant_speech("Проверь свой интернет!")
        return recognized_data


if __name__ == "__main__":
    commands_dict = {
        'commands': {
            'greeting': ['привет', 'здравствуй', 'здравствуйте',
            'добрый', 'день', 'вечер', 'утро',
            'доброго', 'времени', 'суток',
            'приветствую', 'здравствуйте', 'приветствую вас',
            'приветик', 'здорово', 'хай'],
            'introduce': ['расскажи', 'о себе', 'кто', 'ты']

        }
    }
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
