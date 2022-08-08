from mido import MidiFile
import music21
import os

#----SONGS----
#songs in other keys
song='OnlineMidi.mid' #song in d minor
#song='CMajScale.mid'


# unacceptable songs
#song='ID - Nyan Cat.mid' # polyphonic


#-----GLOBAL VARIABLES-----

songName = song[:-4] # name of song

# Use notes instead of MC Note numbers?
# True yes, False no: changes to lowercase on export for lua
notesNotation = True

# Choose instrument
inst = "bass"

# Choose volume
volume = 3

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


#-----FUNCTIONS-----
def parseMidiTime():
  #rplaces = 4 # num of decimal places to round combined time
  timings = []
    #parse midi file
  for msg in MidiFile(song):
    state = msg.type # state is type of message
    #print(msg)
    # check if state is an on or off signal
    if state=="note_on": 
      noteOnTime = msg.time
      #print(noteOnTime)
    if state=="note_off":
      combinedTime = (noteOnTime + msg.time)
      #print(combinedTime)
      #add together on and off times for total note duration
      timings.append(combinedTime) 
  return timings
  
def checkPhonic(): #check if file is monophonic
  lastState = "note_off" # init last state
  for msg in MidiFile(song): #iterate messages
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
  #iterate through all non-meta messages
  for msg in MidiFile(song): 
    state = msg.type
    if state=="note_on":
      note = msg.note
      # update lowest or highest note
      if note < lowest:
        lowest = note
      if note > highest:
        highest = note
  #calculate if note range meets specs
  if (highest-lowest) <= 25:
    return True
  else:
    return False


def scaleRange(): # reports highest and lowest note values
  lowest = 128
  highest = 0
  #iterate through all non-meta messages
  for msg in MidiFile(song):
    state = msg.type
    if state=="note_on":
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
  
def convSong(): 
  score = music21.converter.parse(song)
  key = score.analyze('key')
  print("found", key,"\n")
  keyName = str(key)
  keyName = keyName[:2].upper() + keyName[2:]
  return writeConvList(key, score)

def writeConvList(key, score):
  notes = []
  octs = []
  majors = dict([("A-", -2),("A", -3),
                 ("B-", -4),("B", -5),
                 ("C", -6),("D-", 5),
                 ("D", 4),("E-", 3),
                 ("E", 2),("F", 1),
                 ("F#", 0),("G", -1)])
  minors = dict([("G#", -5),("A", -6),
                 ("B-", 5),("B", 4),
                 ("C", 3),("D-", 2),
                 ("D", 1),("E-", 0),
                 ("E", -1),("F", -2),
                 ("G-", -3),("G", -4)])
  if key.mode == "major":
    halfSteps = majors[key.tonic.name]    
  elif key.mode == "minor":
    halfSteps = minors[key.tonic.name]
  newscore = score.transpose(halfSteps)
  timings = parseMidiTime()
  
  for n in newscore.flat.notes:
    if "-" in n.pitch.name:
      notes.append([n.pitch.name[0]+"b"])
    else:
      notes.append([n.pitch.name])
    octs.append(n.octave)
    
  m = min(octs)
  for i in range(len(notes)):
    if octs[i] == m:
      notes[i][0]+="1"
    elif octs[i] == (m+1):
      notes[i][0]+="2"
    else:
      notes[i][0]+="3"
  
  # TODO add octave number to pitch name
  for x in range(len(notes)):
    notes[x].append(timings[x])
  return formatSongFile(notes)
  

  #print(notes)
def formatSongFile(notes):
  formSong = "--Converted track %s \n\ntrack = {}\n\n"%songName
  for x in range(len(notes)):
    formSong += "track[%i] = {\"%s\", %d, \"%s\", %s}\n"%(x+1, inst, volume, str(notes[x][0]), str(notes[x][1]))
  formSong += "\nmessage = {\"%s\", track, 1, %s}"%(songName,           
              str(notesNotation).lower())
  return(formSong)

def main():
  # check if midi is monophonic and in a 25 note range
  phonic = checkPhonic()
  range = checkRange()
  if phonic and range:
    print("song meets specifications\n")
    formattedSong = convSong()
    print("File preview below:\n"+("---"*5)+"\n\n")
    print(formattedSong)
    if not os.path.exists("./converted-songs"):
      os.mkdir("./converted-songs")
    convertedFile = open(("./converted-songs/" + songName + 
                          "-converted.lua"), "w")
    convertedFile.write(formattedSong)
    convertedFile.close()
    print("File written")

  # if song does not meet specs            
  else:
    print("song does not meet specifications")
    if not phonic:
      print("song is not monophonic")
    if not range:
      print("song has too large of a note range")

main()
