from gtts import gTTS
import os

def text_to_speech(command, voice):
  # The text that you want to convert to audio
  # for i in range(0, len(command)):
  #   if command[i] == '.' and command[i-1].isdigit():
  #     command[0:i] + " point " + command[i+1:]
  if (voice == False):
    return
  c = list(command)
  for i in range(0, len(c)):
    if c[i].isdigit() and c[i+1] == '.' and c[i+2].isdigit():
      c[i+1] = 'point'
  print(str(c))
  mytext = ''.join(str(e) for e in c)
  
  # Language in which you want to convert
  language = 'en'
  
  # Passing the text and language to the engine, 
  # here we have marked slow=False. Which tells 
  # the module that the converted audio should 
  # have a high speed
  myobj = gTTS(text=mytext, lang=language, slow=False)
  
  # Saving the converted audio in a mp3 file named
  # welcome 
  myobj.save("response.mp3")
  
  # Playing the converted file
  os.system("mpg321 response.mp3")
