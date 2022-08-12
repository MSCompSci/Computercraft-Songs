import music21
import sys
import os

#---------------GLOBAL VARIABLES---------------
song = "" # song to convert

# Use notes instead of MC Note numbers?
# changes to lowercase on export for lua
# True by default
notesNotation = True

inst = "" #Instrument that plays note
volume = "" # Volume note plays at

#--------------CONFIGURATION FUNCTIONS---------------
def configSong(): # set song file name
  global song
  midis = [] #
  for x in os.listdir():
    if x.endswith(".mid"):
      midis.append(x)
  selected = False
  while not selected:
    print('Select MIDI file to convert\nMust be in main.py directory to be selectable')
    for y in range(len(midis)):
      print("[",y,"]","  ",midis[y],sep="")
    print("[",len(midis)+1,"]","  Exit program",sep="")
    file = input('Selection: ')
    print("\n")
    if file.isnumeric(): # select only midi files
      file = int(file)
      if (file <= (len(midis)-1)) and not (file<0):
        song = midis[int(file)] #assign song file name globally
        selected = True
        print("\n")
        print("File selected:",song,"\n")
      elif file == (len(midis) + 1):
        sys.exit()
      else:
        print("Invalid selection\n")
  return True

def useConf(): #check if user wants to use configuration file
  global noteNotation
  global inst
  global volume
  if os.path.isfile("./config.txt"): #check if config exists
    print("Configuration file found.")
    a = input("Apply saved configuration? [Y/N]: ") #ask user if config should be applied
    while a not in ['y', 'Y', 'n', 'N']:
      print("Invalid input")
      a = input("Apply saved configuration? [Y/N]: ")
    if a in ["y","Y"]: # if yes
      print("\n")
      #read config
      f = open("config.txt","r") 
      for line in f.readlines():
        fln = line.rstrip().split(',')
      #apply config to global variables
      noteNotation = fln[0]
      inst = fln[1]
      volume = fln[2]
      #print(noteNotation, inst, volume)
      return True
    else: # if no
      print("\n")
      return False
  else: # if config does not exist
    return False
  

def configNot(): #configure notation style
  global notesNotation
  no = input("Use letter note notation (A, Bb, etc.) or Minecraft Number notation (0-24)? [L/N]: ") 
  while no not in ['l', 'L', 'n', 'N']:
    print("Invalid input")
    no = input("Use letter note notation (A, Bb, etc.) or Minecraft Number notation (0-24)? [L/N]: ")
  if no == "N":
    notesNotation = False
    print("Using Minecraft Number notation\n")
  else:
    print("Using Letter notation\n")
    
def configInst():
  global inst
  # List of minecraft accepted instruments
  instList = ["harp", "basedrum", "snare", "hat", "bass", "bell", "guitar", "chime", "xylophone", "iron_xylophone", "cow_bell", "didgeridoo", "bit", "banjo", "pling"]
  print("Select midi instrument from list:\n")
  for x in range(len(instList)):
    print("["+str(x)+"]",instList[x])
  print("\n")
  numState = False
  while numState == False: # verify user selection
    number = input("Enter instrument number: ")
    if not number.isnumeric():
      print("Invalid input: not a number")
    elif int(number) not in range(len(instList)):
      print("Invalid input: number not in range")
    else:
      numState = True
      inst = instList[int(number)] #assign chosen instrument globally
      print("Instrument selected:",inst,"\n")
      
def configVol():
  global volume
  volumes = "1, 2, 3" # Minecraft accepted volume values
  numState = False # verify input volume value
  while numState == False:
    v = input("Enter volume (" + volumes + "): ")
    if not v.isnumeric():
      print("Invalid input: not a number")
    elif int(v) not in range(1,4):
      print("Invalid input: number not in range")
    else:
      numState = True
      volume = v # assign volume value globally
      print("Volume selected:",v,"\n")
      
def confirmConfig(): # confirm selected settings
  global song
  global notesNotation
  global inst
  global volume
  # display selected settings
  print("Settings selected:\n")
  print("\tFile selected:",song,"\n")
  if notesNotation == False:
    print("\tUsing Minecraft Number notation\n")
  else:
    print("\tUsing Letter notation\n")
  print("\tInstrument selected:",inst,"\n")
  print("\tVolume selected:",volume,"\n")
  correct = input("Are these settings correct? [Y/N]: ")
  while correct not in ['y', 'Y', 'n', 'N']:
    print("Invalid input, try again")
    correct = input("Are these settings correct? [Y/N]: ")
  if correct in ["n","N"]:
    print("\n")
    return False
  else:
    print("\n")
    return True
    

    
def mkConfig(): # make configuration file
  global notesNotation
  global inst
  global volume
  mk = input("Save notation, instrument, and volume settings as configuration file? (y/n): ")
  while mk not in ['y', 'Y', 'n', 'N']:
    print("Invalid input, try again")
    mk = input("Save notation, instrument, and volume settings as configuration file? [Y/N]: ")
  if mk in ["y","Y"]: # if yes, write to config.txt
    conf = [notesNotation, inst, volume] # configured values
    try:
      f = open("config.txt","w")
      for i in conf[:-1]:
        f.write(str(i)+", ")
      f.write(str(conf[-1]))
      f.close()
    except Exception as e: # handle exception and try again
      print("ERROR: File could not be written\n")
      print(e)
      print("Configuration must be set manually")
      return False
    else:
      return True
      
      
      
def askExit(): # ask user if program should be restarted or exited
  ex = input("Do you want to restart the program? [Y/N]: ")
  while ex not in ['y', 'Y', 'n', 'N']: # filter for y/n
    print("Invalid input, try again")
    ex = input("Do you want to restart the program? [Y/N]: ")
  if ex in ["n","N"]: # if no, exit program
    sys.exit()  
  else:
    config() # TODO            

def config():
  confirmed = False
  confIssue = False
  while not confirmed: # while settings are not confirmed
    if configSong(): # set song file name
      confirmed = True 
      conf = True
      if not useConf(): # if config file not used
        conf = False
        configNot() # set notation style
        configInst() # set instrument
        configVol() # set volume
      if confirmConfig(): # confirm settings
        if not conf and not confIssue:
          if mkConfig(): # ask to save as config file
            confirmed = True
          else:
            confIssue = True
      else: # ask if user wants to exit or restart if settings are incorrect
        confirmed = True
        askExit()
  

#---------------MIDI PARSING FUNCTIONS---------------
def parseMidi(song): # parse midi file
  
  '''Begin modified snippet based on https://gist.github.com/aldous-rey/68c6c43450517aa47474#file-transposer-py'''
  score = music21.converter.parse(song) # parse midi to stream
  key = score.analyze('key') # find music key
  #print("found", key,"\n")     
  # step values for transposition to F#
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
  # set half steps to transpose
  if key.mode == "major":
    halfSteps = majors[key.tonic.name]    
  elif key.mode == "minor":
    halfSteps = minors[key.tonic.name]
  newscore = score.transpose(halfSteps) # transpose music stream
  # make stream only notes, chords, and rests
  newscore = newscore.flat.notesAndRests
  ''' End modified snippet '''
  
  noteList = [[]] # init list for notes and values
  offset = 0.0 # init offset from beginning of track
  # set up noteList
  for x in newscore:
    if x.offset > offset:
      noteList.append([])
      offset = x.offset
  offset = 0.0 # reset offset
  i = 0 # init index counter
  # fill noteList with note names, midi values, and offsets
  for n in newscore:
    t = str(type(n)) # type of item to compare
    
    # increment through index of noteList 
    # for each set of notes with the same offset value
    if n.offset != offset: 
      i += 1
      offset = n.offset # set offset to new baseline
    if 'Note' in t: # filter for notes
      name = n.name # select note name
      if "-" in name: # replace "-" with "b" in flat notes
        name = name[:-1] + "b"  
      noteList[i].append([name, n.pitch.midi, n.offset]) # add note
    
    elif 'Chord' in t: # extract chords into seperate notes
      for c in n: 
        name = c.name # select note name
        if "-" in name: # replace "-" with "b" in flat notes
          name = name[:-1] + "b"
        noteList[i].append([name, c.pitch.midi, n.offset]) # add note
  if noteList[-1] == []:
    del noteList[-1]
  return noteList

def checkRange(s): # check range of score "s"
  maxNote = -1 # set baseline for max/min midi values in score
  minNote = 128 
  for m in s: # iterate blocks of notes with same offset
    for n in m: # iterate notes in blocks
      #set new max/min midi values if encountered
      if n[1] > maxNote:
        maxNote = n[1]
      if n[1] < minNote:
        minNote = n[1]
  # return multiple values
  s = maxNote - minNote
  a = [minNote, maxNote, s]
  return a

def addOct(s,minNote,maxNote): # Add MC Octave number
  # tuple of F# midi values
  fs = (6, 18, 30, 42, 54, 66, 78, 90, 102, 114, 126) 
  
  # set extreme high and low end scale cases
  # NOTE: these are unlikely but possible: midi values range from 0-127
  if minNote < 6:
    midFS = 6
    highFS = 18
    lowFS = -1
  elif maxNote > 114:
    midFS = 114
    highFS = 129
    lowFS = 102
  else: # set F# octave boundaries from tuple value comparison
    for x in range(len(fs)):
      if minNote >= fs[x]:
        lowFS = fs[x]
        midFS = fs[x] + 12
        highFS = fs[x] + 24
        
    for m in s: # iterate blocks of notes with same offset
      for n in m: # iterate notes in blocks
        if "F#" not in n[0]: # select only non-F# notes
          if (n[1] < highFS) and (n[1] > midFS): # set middle octave
              n[0] += "2"
          else: # set low octave 
            n[0] += "1"
          #NOTE: only F# has a high octave
            
        else: # set F# octaves by direct comparison
          if n[1] == highFS:
            n[0] += "3"
          elif n[1] == lowFS:
            n[0] += "1"
          else:
            n[0] += "2"
  return s
  
def assignSpeaker(s): # assign speaker channel number
  for m in s: # iterate blocks of notes with same offset
    speaker = 1
    for n in m: # iterate notes in blocks
      n.append(speaker)
      speaker += 1
  return s

  
def addTiming(s): # add note duration timing by speaker
  #iterate through parsed song notes
  for m in range(len(s)):
    for n in range(len(s[m])):
      # set baseline for smallest difference between offsets
      smallestDiff = 128 
      # iterate through all notes after current note
      for x in range(m,len(s)):
        for y in range(len(s[x])):
          if s[m][n][-1] == s[x][y][-1]: # find notes with same speaker
            if s[x][y][-2] > s[m][n][-2]: # find notes with larger offset
              diff = s[x][y][-2] - s[m][n][-2] # calc offset difference
              # set new smallest offset between notes of same speaker
              if (diff) <smallestDiff: 
                smallestDiff = diff
            # set offset difference of 1 for notes at end of piece 
            # this gives them a duration
            elif m == (len(s)-1): 
              smallestDiff = 1.0
      # multiplier to adjust to reasonable bpm 
      #(est 120, can be adjusted with tempo multiplier in song file later)
      adjustToSeconds = 0.5 
      # insert note duration after note name for each note in s
      s[m][n].insert(1,smallestDiff*adjustToSeconds) 
  return s
      
def formatLua(s): # format song for lua file
  global song
  global inst
  global volume
  global notesNotation
  songName = song[:-4] # song name is midi file name without the extension
  
  # first line of lua
  formattedS = "--Converted track %s\n\ntrack = {}\n\n"%songName
  i = 1 # index for track{} in lua file
  
  # assign track indeces 
  for m in s:
    for n in m:
      # lua track format: 
      # track[i] = {"inst, volume, note name, note duration, speaker number"}
      formattedS += "track[%d] = {\"%s\", %s, \"%s\", %s, %s}\n"%(i, inst, volume, n[0], n[1], n[-1])
      i += 1
  # add message encapsulating line 
  # format: message = {song name, track, tempo multiplier(1 by default), notesNotation(lowercase for lua)}
  formattedS += "\nmessage = {\"%s\", track, 1, %s}"%(songName,           
              str(notesNotation).lower())
  return formattedS

def writeLua(fs): # write formatted song to lua file
  global song
  songName = song[:-4] # set song name to midi file name without extension
  fileName = songName + "-converted.lua" # set lua file name default
  print("All converted files will be saved in \"converted-songs\" folder\n")
  msg = ("(Y) Save as %s\n(N) Choose new file name\n[Y/N]: ")%fileName
  mk = input(msg) # ask user about file name options
  print("\n")
  while mk not in ['y', 'Y', 'n', 'N']:
    print("Invalid input, try again")
    mk = input(msg)
    print("\n")
  if not os.path.exists("converted-songs"): # check if directory exists
      os.mkdir("converted-songs") # make if it DNE

  # test user input file name
  x = False
  while x == False:
    if mk in ["n","N"]: # write to non-standard file name
      print("File can be saved as either .txt or .lua")
      print("File defaults to .lua\n")
      fileName = input("Enter file name: ")
      # check if file name contains a txt or lua extension
      if not (".lua"==fileName[-4:] or ".txt"==fileName[-4:]):
        if "." in fileName: # if not, either remove other ext and add one...
          fileName = fileName[:fileName.index(".")] + ".lua"
        else: #... or add one if one is not added already
          fileName += ".lua"
    try: # try writing file to converted-songs dir
      pathName = os.path.join("converted-songs", fileName)
      f = open(pathName, "w")
      f.write(fs)
      f.close()
    except Exception as e: # handle exception and try again
      print("ERROR: File could not be written\n")
      print(e)
    else: # file was written correctly
      x = True
      
#---------------MAIN---------------
def main():
  global song
  global midiList
  global score
  print("-"*15 + "CONFIGURATION" + "-"*15 + "\n")
  config() # run settings config
  print("-"*15 + "MIDI-CONVERSION" + "-"*15 + "\n")
  print("Begin parsing...",end=" ")
  parsedSong = parseMidi(song) # parse midi and transpose
  print("MIDI parsed\n")
  a = checkRange(parsedSong)
  minNote = a[0]
  maxNote = a[1]
  
  if a[2] <= 25: # check if song is within 25 note MC range
    print("Song within range\n")
    parsedSong = addOct(parsedSong,minNote,maxNote)
    print("Minecraft octave numbers added\n")
    parsedSong = assignSpeaker(parsedSong)
    print("Speakers assigned\n")
    parsedSong = addTiming(parsedSong)
    print("Note timing added\n")
    print("Formatting for Lua export...", end="")
    formattedSong = formatLua(parsedSong)
    print("Formatted\n")
    writeLua(formattedSong)
    print("File saved!\n")

    
  else:
    print("Song not in 25 note range\n")
    askExit()

main()
