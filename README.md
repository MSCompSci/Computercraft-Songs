# Computercraft-Songs
### Song system for Minecraft Computercraft Speakers
___

This is a project to allow the creation of custom songs that can then be sent to remote client speakers using the [Computercraft: Tweaked](https://tweaked.cc/) Minecraft mod.

`We are not sponsored by, or affiliated with Mojang, Computercraft: Tweaked, or any other mentioned projects or resources.`

## How it works

All songs are stored on a main Computercraft computer that acts as a server. This server then sends the song files to linked client computers that play the song's notes through their attached speakers.

If the song being played has only one note being played at a time (aka a monophonic song,) then the default client scripts will play every note and you will only need one speaker. However, if the song has more than one note being played at a time in chords, harmonies, etc. (aka a polyphonic song,) then you will need to examine the song file and find the largest speaker number listed. That will tell you the minimum number of speakers you need, and you will need to set at least one speaker to each speaker number in its client file in order to fully play a song.

### Song files

Each song file is made of several parts.

1. At the beginning of the file is a comment with the name of the song
2. Then the `track` array is initiallized with `track = {}`
3. Each note of the song is added to the `track` array at index `i` using the following format:
    - the Minecraft noteblock instrument (see the [Minecraft Wiki](https://minecraft.fandom.com/wiki/Note_Block#Instruments) for a list of instruments.
    - the volume (0-3, `3` is default. See [ComputerCraft: Tweaked](https://tweaked.cc/peripheral/speaker.html#v:playNote) for more info.)
    - the note in either standard western music notation or Minecraft noteblock numbers
    - the note duration as a portion of a whole note (1 is a whole note, 0.5 is a half note etc.)
    - which speaker the note will play from as a number (`1` is default)
        ```lua
        track[ i ] = {instrument, volume, note, duration, speaker}
        ```
4. The song file ends by wrapping the **track** array in **message** along with:
    - the song name
    - the name of the array (`track` is default)
    - a tempo multiplier that can be used to manually adjust the speed of playback (`1` is default)
    - and `true` if the song file uses music notation like **"F#1"** or `false` if the Minecraft note block numbers 0-24 are used.
    - This is written in the format
        ```lua
        message = {songName, track, tempoMultiplier, notationBoolean}
        ```

### Server scripts

The server.lua script allows you to send a song to multiple client computers once a redstone signal is recieved. You can configure which songfile and client group are used when the script is run. `group` is the default group name.
```lua
shell.run("server.lua", "path/to/songfile.lua", "groupName"). 
```

The server_pocket.lua script can be used if you wish to have the server automatically transmit the song on startup.

### Client script

The client.lua script allows a client computer to recieve the streamed message from the server, apply the decoder script to it if the song uses note notation instead of Minecraft note block numbers, and then play the song to a connected speaker.

This script also allows you to recieve and run code sent to the client from the server for updates etc.

### Server Hardware

The server is the computer that will send information to other client computers. To do this, you will need to attach a [modem](https://tweaked.cc/peripheral/modem.html) to the computer. 

The server.lua script also needs an external redstone signal to trigger the process of sending data to the client. This can come from a basic button, lever, or any other redstone signal that can turn on and off. You can find more advanced redstone circuit information on the [Minecraft Wiki](https://minecraft.fandom.com/wiki/Redstone_circuits) for specialized configurations.

### Client Hardware

Each client will need to be a seperate computer and have a [modem](https://tweaked.cc/peripheral/modem.html) to recive information from the server. 

Clients will also need to be connected to [speakers](https://tweaked.cc/peripheral/speaker.html) in order to play music.

## The MIDI converter

This GitHub also contains a midi converter written in python that can automatically format MIDI files to make them playable using these scripts.

#### The MIDI file must have a highest and lowest note that fall within 25 MIDI pitch values (be within a range of 25 half-steps) in order to be convertable

Currently the script is offered with a command line interface only, however we plan to create a graphical version. This script will automatically check if the song meets the note range requirements.

### Installing the MIDI converter
- The MIDI converter makes use of the python library [music21](http://web.mit.edu/music21/), which must be installed in the python environment where the converter is run.
- Installation instructions for music21 on all systems, as well as python on windows can be found [here.](http://web.mit.edu/music21/doc/usersGuide/usersGuide_01_installing.html) 
- The MIDI converter can also be run online if you create a fork of the [Repl live environment repository.](https://replit.com/@mscompsci/MIDI-Test#main.py) You can then upload a MIDI file to convert to the main directory and run the program.



___

## Helpful Resources

### Minecraft

* [Computercraft: Tweaked Wiki](https://tweaked.cc/)

* [Minecraft Wiki: Redstone Circuits](https://minecraft.fandom.com/wiki/Redstone_circuits)

* [Minecraft Wiki: Note Block Note Explanation](https://minecraft.fandom.com/wiki/Note_Block#Notes)

### Music Notation Help

* [Blair School of Music: MIDI note value reference](https://computermusicresource.com/midikeys.html)

* [musicca: Free Online Virtual Piano](https://www.musicca.com/piano)

* [musicnotes.com: How to Read Music for Beginners](https://www.musicnotes.com/now/tips/how-to-read-sheet-music/)

### MIDI Recording and Notation Editing

* [MuseScore3: music notation software](https://musescore.org/en)

* [wikiHow: How to Use MuseScore](https://www.wikihow.com/Use-MuseScore)

* [Cakewalk DAW](https://www.bandlab.com/products/cakewalk)

* [Ardour DAW](https://ardour.org/)
