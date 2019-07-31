from transliterate import translit
from gtts import gTTS
import os

readmefile = open('readme.txt','r')
print(readmefile.read(256))
readmefile.close()


def text2text(textfile, lang):
    result = open('result.txt', 'w')
    for line in textfile:
        result.write(translit(line,lang))
    result.close()

def text2voice(textfile, lang):
    temp = textfile.read()
    tts = gTTS(temp, lang=lang)
    tts.save('result.mp3')

print('''Make your choice.

[T] Text to Text
[V] Text to Voice
[Ctrl+C] to Exit''')
userchoice = input()

original_file = input('Please enter txt filename to transliterate: ')
lang = input('Please enter destination language: ')
textfile = open(original_file,'r')

if userchoice == 'T':
    text2text(textfile,lang)
    textfile.close()
    print('Please check result.txt at the same folder')
elif userchoice == 'V':
    text2voice(textfile,lang)
    textfile.close()
    print('Please check result.mp3 at the same folder')

print('Thank you and good bay. Any questions? Please read readme.txt')
