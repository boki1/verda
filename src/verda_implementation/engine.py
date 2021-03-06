from string import punctuation as PUNCTUATORS
import logging
from .components import DecompositionRuleNotFoundException, ReassemblyRuleNotFoundException, KeywordProcessingFailedException
from .memory import PhraseMemory, Keystack
from enum import IntEnum
from copy import copy as shallow_copy
from .decomposer import Decomposer
from .reassembler import Reassembler
from google_trans_new import google_translator
import speech_recognition as sr
import pyttsx3


class Globals(IntEnum):
    HELLO_IDX = 0
    GOODBYE_IDX = 1


class VerdaEngine:
    def __init__(self):
        self.phrasing_memory = PhraseMemory.instance()
        self.context_memory = []
        self.decomposer = Decomposer(self.context_memory)
        self.reassembler = Reassembler()
        self.quits = list()
        for i in PhraseMemory.goodbye_messages():
            for j in i:
                self.quits.append(j)
        self.done_greetings = [False, False]

    @staticmethod
    def clear_punctuation(sentence: str) -> str:
        logging.debug("Before de-punctuation: '{sentence}'")
        filtered = ''.join(list(filter(lambda symbol: symbol not in PUNCTUATORS, sentence)))
        logging.debug("After de-punctuation: '{filtered}'")
        return filtered

    def only_text(self, text: str, language: str):
        translator = google_translator()
        while True:
            text_en = translator.translate(text)
            print(text_en)
            output = self.answer_to(text_en)
            output = output.capitalize()
            if text_en[:(len(text_en) - 1)].lower() in self.quits:
                self.conversation_end()
                return None
            return output

    def speech_to_text(self, language: str):
        translator = google_translator()
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                try:
                    in_out = list()
                    recognizer.adjust_for_ambient_noise(source)
                    audio_file = recognizer.record(source, duration=5.0)
                    text = recognizer.recognize_google(language=language, audio_data=audio_file)
                    in_out.append(text)

                    text_en = translator.translate(text)
                    output = self.answer_to(text_en)
                    output = output.capitalize()
                    if text_en[:(len(text_en) - 1)].lower() in self.quits:
                        self.conversation_end()
                        return None

                    in_out.append(output)
                    return in_out
                except:
                    pass

    def speech_and_text_to_speech(self, language: str):
        translator = google_translator()
        recognizer = sr.Recognizer()

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty("rate", 150)
        engine.setProperty('voice', voices[2].id)

        with sr.Microphone() as source:
            while True:
                try:
                    in_out = list()
                    recognizer.adjust_for_ambient_noise(source)
                    audio_file = recognizer.record(source, duration=5.0)
                    text = recognizer.recognize_google(language=language, audio_data=audio_file)
                    in_out.append(text)

                    text_en = translator.translate(text)
                    output = self.answer_to(text_en)
                    if text_en[:(len(text_en) - 1)].lower() in self.quits:
                        engine.say(translator.translate(self.conversation_end(), lang_tgt=language))
                        engine.runAndWait()
                        return None
                    engine.say(translator.translate(output, lang_tgt=language))
                    engine.runAndWait()
                    in_out.append(output)
                    return in_out
                except:
                    pass

    def text_to_speech(self, text: str, language: str):
        translator = google_translator()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty("rate", 150)
        engine.setProperty('voice', voices[2].id)
        while True:
            text_en = translator.translate(text)

            output = self.answer_to(text_en)
            output = output.capitalize()
            if text_en[:(len(text_en) - 1)].lower() in self.quits:
                engine.say(translator.translate(self.conversation_end(), lang_tgt=language))
                engine.runAndWait()
                return None
            engine.say(translator.translate(output, lang_tgt=language))
            engine.runAndWait()
            return output

    def loop(self):
        if not self.done_greetings[Globals.HELLO_IDX]:
            self.conversation_begin()

        language = input("Enter language (bg / en / ru / de): ")
        speech = input("Do you want to speak to Verda (y / n): ") == 'y'
        text_to_speech = input("Do you want Verda to speak (y / n): ") == 'y'

        quits = list()
        for i in PhraseMemory.goodbye_messages():
            for j in i:
                quits.append(j)

        text = input("> ")
        if not speech and not text_to_speech:
            self.only_text(text, language)
        elif speech and not text_to_speech:
            self.speech_to_text(language)
        elif speech and text_to_speech:
            self.speech_and_text_to_speech(language)
        elif not speech and text_to_speech:
            self.text_to_speech(text, language)

    def answer_to(self, question: str) -> str:
        sentence = self.clear_punctuation(question)
        sentence = sentence.lower()
        keywords = Keystack(sentence, shallow_copy(self.phrasing_memory))
        keywords = keywords.prioritize()

        subs = dict(PhraseMemory.pre_substitutors())
        words = sentence.split(' ')
        words = Reassembler.replace(words, subs)
        sentence = ' '.join(words)

        response = ""

        try:
            response: str = self.decomposer.process_keywords(keywords, sentence)
        except ReassemblyRuleNotFoundException as r_err:
            logging.exception(r_err.msg)
        except DecompositionRuleNotFoundException as d_err:
            logging.exception(d_err.msg)
        except KeywordProcessingFailedException as k_err:
            logging.exception(k_err.msg)

        return response


    def conversation_begin(self):
        print(PhraseMemory.hello_greeting())
        self.done_greetings[Globals.HELLO_IDX] = True

    def conversation_end(self):
        print(PhraseMemory.goodbye_greeting())
        self.done_greetings[Globals.GOODBYE_IDX] = True
