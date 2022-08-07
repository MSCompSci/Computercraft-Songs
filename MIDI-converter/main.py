from mido import MidiFile
import music21
#twinkle is monophonic
#twinkle-twinkle-little-star is polyphonic

#song = 'twinkle.mid'
#song = 'twinkle-twinkle-little-star.mid'
song='OnlineMidi.mid' #song not in c but is monophonic
#song='ID - Nyan Cat.mid'


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

def checkRange():
  lowest = 128
  highest = 0
  for msg in MidiFile(song):
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
  print("highest:",highest,"lowest:",lowest)
  #mcNotes = []




def convKey(): #TODO change key to G flat (aka F# or mc 0) major and rel minor
  #adapted snippet from https://gist.github.com/aldous-rey/68c6c43450517aa47474#file-transposer-py
  score = music21.converter.parse(song)
  key = score.analyze('key')
  print("found", key)
  if str(key) != ("C major" or "A minor"):
    print("Converting key")

    # original majors = dict([("A-", 4),("A", 3),("B-", 2),("B", 1),("C", 0),("D-", -1),("D", -2),("E-", -3),("E", -4),("F", -5),("G-", 6),("G", 5)])
    #original minors = dict([("A-", 1),("A", 0),("B-", -1),("B", -2),("C", -3),("D-", -4),("D", -5),("E-", 6),("E", 5),("F", 4),("G-", 3),("G", 2)])
    # major conversions
    majors = dict([("A-", 4),("A", 3),("B-", 2),("B", 1),("C", 0),("D-", -1),("D", -2),("E-", -3),("E", -4),("F", -5),("G-", 6),("G", 5)])

    # like majors - 3
    minors = dict([("A-", 1),("A", 0),("B-", -1),("B", -2),("C", -3),("D-", -4),("D", -5),("E-", 6),("E", 5),("F", 4),("G-", 3),("G", 2)])
    if key.mode == "major":
      halfSteps = majors[key.tonic.name]    
    elif key.mode == "minor":
      halfSteps = minors[key.tonic.name]
    newscore = score.transpose(halfSteps)
    file = song[:-4] + " MC converted.mid"
    newscore.write("midi", file)
  else:
    print("Key does not need to be converted")


noteVals = {"C":(0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120),
            "D":(2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122),
            "E":(4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124),
            "F":(5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125),
            "G":(7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127),
            "A":(9, 21, 33, 45, 57, 69, 81, 93, 104, 117),
            "B":(11, 23, 35, 47, 59, 71, 83, 95, 107, 119)
           }
phonic = checkPhonic()
range = checkRange()
if phonic and range:
  print("song meets specifications")

  #Check if key needs to be converted
  # if so, make new midi file in new key
  convKey()

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
