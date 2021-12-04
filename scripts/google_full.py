import sys
import moviepy.editor as mp
import os
import time
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from nemo.collections.nlp.models import PunctuationCapitalizationModel
from string import ascii_letters
from flair.models import TextClassifier
from flair.data import Sentence
#import speech_recognition as sr



SetLogLevel(0)
classifier = TextClassifier.load('en-sentiment')

def flair_prediction(x):
    sentence = Sentence(x)
    classifier.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "/pos/{}".format(str(score).split(' ')[-1])
    elif "NEGATIVE" in str(score):
        return "/neg/{}".format(str(score).split(' ')[-1])
    else:
        return "/neu/{}".format(str(score).split(' ')[-1])


def converter(video_filename):
    clip = mp.VideoFileClip(video_filename)
    audio_filename = video_filename.split('.')[0].split('/')[1]
    audio_filename = 'audio/' + audio_filename + '.wav'
    clip.audio.write_audiofile(audio_filename, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
    return audio_filename

def recongize_vosk(audio_filename, text_filename, model_path='model'):

    #print(f"Reading your file '{audio_filename}'...")
    wf = wave.open(audio_filename, "rb")
    #print(f"'{audio_filename}' file was successfully read")

    # check if audio if mono wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit()

    print(f"Reading your vosk model '{model_path}'...")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    print(f"'{model_path}' model was successfully read")

    print('Start converting to text. It may take some time...')

    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)




    # forming a final string from the words
    text = ''
    list_words = []
    for r in results:
        text += r['text'] + ' '
        if len(r)==1:
            continue
        for obj in r['result']:
            list_words.append(str(obj['start']) +'/'+ str(obj['end']) +'/'+ obj['word'])

    model = PunctuationCapitalizationModel.from_pretrained("punctuation_en_bert")
    output = model.add_punctuation_capitalization([text])
    result = []
    clean_text = output[0].split('. ')
    ind = 0
    for sentence in clean_text:
        pred = flair_prediction(sentence)
        words = sentence.split(' ')
        first = words[0]
        clean_first = ''.join([letter for letter in first if letter in ascii_letters])
        last = words[-1]
        clean_last = ''.join([letter for letter in last if letter in ascii_letters])
        start = '0'
        end = '0.1'
        #print(clean_first + " " + clean_last)
        for i in range(ind, len(list_words)):
            temp = list_words[i].split('/')
            temp_start = temp[0]
            temp_end = temp[1]
            temp_word = ''.join([letter for letter in temp[2] if letter in ascii_letters])
            if clean_first.lower() == temp_word:
                start = temp_start
                end = temp_end
                clean_first = '-1'
            elif start!='0' and clean_last.lower() == temp_word:
                end = temp_end
                ind+=1
                break
            ind+=1
        result.append(sentence + '/' + start + '/' + end + pred)

    with open(text_filename, "w") as text_file:
        for word in result:
            text_file.write(word+'\n')
    print(f"Text successfully saved")
    return result

def main(video_filename):

    # extract audio file in wav mono format from input video and save in audio/ folder
    #audio_filename = converter(video_filename)
    audio_filename = video_filename
    text_filename = audio_filename[:-3] + 'txt'
    # 
    return recongize_vosk(audio_filename, text_filename)


#if __name__ == "__main__":
#    main()

def get_prediction_audio(x):
    return main(x)