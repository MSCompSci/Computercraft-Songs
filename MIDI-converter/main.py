from mido import MidiFile
import music21

#Global Variables
#song = 'twinkle.mid' #twinkle is monophonic in C maj
#song = 'twinkle-twinkle-little-star.mid' #twinkle-twinkle-little-star is polyphonic
#song='OnlineMidi.mid' #song in d minor
song="GMaj.mid"
#song='ID - Nyan Cat.mid' # polyphonic
#songs that don't need to be converted
#song="EflatMin.mid"
#song="Fsharp.mid"

# MIDI note values
noteVals = {"C":(0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120),
            
            "C#":(1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121),
            #"Db":(1, 13, 25, 37, 49, 61, 73, 85, 97, 109, 121),
            
            "D":(2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122),

            "D#":(3, 15, 27, 39, 51, 63, 75, 87, 99, 111, 123),
            #"Eb":(3, 15, 27, 39, 51, 63, 75, 87, 99, 111, 123),
            
            "E":(4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124),
            
            "F":(5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125),
            
            "F#":(6, 18, 30, 42, 54, 66, 78, 90, 102, 114, 126),
            #"Gb":(6, 18, 30, 42, 54, 66, 78, 90, 102, 114, 126),
            
            "G":(7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127),

            "G#":(8, 20, 32, 44, 56, 68, 80, 92, 104, 116),
            #"Ab":(8, 20, 32, 44, 56, 68, 80, 92, 104, 116),
            
            "A":(9, 21, 33, 45, 57, 69, 81, 93, 104, 117),
            
            "A#":(10, 22, 34, 46, 58, 70, 82, 94, 106, 118),
            #"Bb":(10, 22, 34, 46, 58, 70, 82, 94, 106, 118),
            
            "B":(11, 23, 35, 47, 59, 71, 83, 95, 107, 119)
           }

# Minecraft Note Block Values
#mcNotes = 

def checkPhonic(): #check if file is monophonic
  lastState = "note_off" # init last state
  for msg in MidiFile(song): #iterate messages
      if not msg.is_meta: # only check non-metadata
          state = msg.type # state is type of message
          # check if state is an on or off signal
          if state=="note_on" or state=="note_off":
            # compare with last state to prevent 2 on signals
            # being active at the same time (polyphonic)
            if state != lastState:
              lastState = state
            else:
              return False #not monophonic
  return True # monophonic

def checkRange(): # Check if highest and lowest note values are within 25 notes
  
  lowest = 128
  highest = -1
  for msg in MidiFile(song): #iterate through all non-meta messages
    if not msg.is_meta:
      state = msg.type
      if state=="note_on":
        note = msg.note
        if note < lowest:
          lowest = note
        if note > highest:
          highest = note
  if (highest-lowest) <= 25:
    return True
  else:
    return False


def scaleRange():
  print(song)
  lowest = 128
  highest = 0
  for msg in MidiFile(song):
    if not msg.is_meta:
      state = msg.type
      if state=="note_on" or state=="note_off":
        note = msg.note
        if note < lowest:
          lowest = note
        if note > highest:
          highest = note
  for n in noteVals:
    if lowest in noteVals[n]:
      print(n, lowest)
    if highest in noteVals[n]:
      print(n, highest)
  print("highest:",highest,"lowest:",lowest)
  
def convKey(): #TODO change key to G flat (aka F# or mc 0) major and rel minor
  #adapted snippet from https://gist.github.com/aldous-rey/68c6c43450517aa47474#file-transposer-py
  score = music21.converter.parse(song)
  key = score.analyze('key')
  print("found", key)
  keyName = str(key)
  keyName = keyName[:2].upper() + keyName[2:]
  if (keyName != "F# major") and (keyName != "E- minor"):
    print("Converting key")
    newSong = writeConvFile(key, score)
    #newScore = music21.converter.parse(newSong)
    #newKey = newScore.analyze('key')
    #print("found", newKey)
    return newSong

  else:
    print("Key does not need to be converted")
    return song

def writeConvFile(k, s):
  key = k
  score = s
  majors = dict([("A-", -2),("A", -3),("B-", -4),("B", -5),("C", -6),("D-", 5),("D", 4),("E-", 3),("E", 2),("F", 1),("F#", 0),("G", -1)])
  minors = dict([("G#", -5),("A", -6),("B-", 5),("B", 4),("C", 3),("D-", 2),("D", 1),("E-", 0),("E", -1),("F", -2),("G-", -3),("G", -4)])
  if key.mode == "major":
    halfSteps = majors[key.tonic.name]    
  elif key.mode == "minor":
    halfSteps = minors[key.tonic.name]
  newscore = score.transpose(halfSteps)
  file = song[:-4] + " MC converted.mid"
  newscore.write("midi", file)
  return file
  

def parseMidi():
    #parse midi file
  for msg in MidiFile(song):
    if not msg.is_meta: # only check non-metadata
      state = msg.type # state is type of message
      # check if state is an on or off signal
      if state=="note_on" or state=="note_off":
        #check which note corresponds to the midi value
        for n in noteVals:
          if msg.note in noteVals[n]:
            print(n, msg.note)




def main():
  global song
  
  phonic = checkPhonic()
  range = checkRange()
  if phonic and range:
    print("song meets specifications")
    parseMidi()
    song = convKey()
    print(song)
    #parseMidi()
    #convKey()
    scaleRange()
    
  # if song does not meet specs            
  else:
    print("song does not meet specifications")
    if not phonic:
      print("song is not monophonic")
    if not range:
      print("song has too large of a note range")
  
  
  # TODO figure out lowest note to put as lower octave in mc scale
  # and fit rest of scale accordingly

main()
