# Computercraft-Songs
### Song system for Minecraft Computercraft Speakers
___

This is a project to allow the creation of custom songs that can then be sent to remote client speakers using the [Computercraft: Tweaked](https://tweaked.cc/) Minecraft mod.

## How it works

All songs are stored on a main Computercraft server. This server then sends the song files to linked client computers that play the song's notes through their attached speakers.

If the song being played has only one note being played at a time (aka a monophonic song,) then the default client scripts will play every note and you will only need one speaker. However, if the song has more than one note being played at a time in chords, harmonies, etc. (aka a polyphonic song,) then you will need to examine the song file and find the largest speaker number listed. That will tell you the minimum number of speakers you need, and you will need to set at least one speaker to each speaker number in its client file in order to fully play a song.

### Song files

Each song file is made of several parts.

1. At the beginning of the file is a comment with the name of the song
2. Then the **Track** array is initiallized with **"Track = {}"**
3. Each note of the song is added to the **Track** array at index **"i"** using the following format
    - **track[ i ] = { instrument, volume, note, duration, speaker }**
4. The song file ends by wrapping the **Track** array in **message** along with:
    - the song name 
    - a tempo multiplier that can be used to manually adjust the speed of playback
    - and *true* if the song file uses letters like **"F#1"** or *false* if the Minecraft note block corresponding numbers 0-24 are used.
    - This is written in the format:
        - **message = {song Name, track, 1 (this is default for the tempo muliplier), false}

### Server script
### Client script
### Server and client installation
### Updating clients

## The MIDI converter

This GitHub also contains a midi converter written in python that can automatically format MIDI files to make them playable using these scripts.

#### The MIDI file must have a highest and lowest note that fall within 25 MIDI pitch values (be within a range of 25 half-steps) in order to be convertable

Currently the script is offered with a command line interface only, however we plan to create a graphical version. This script will automatically check if the song meets the note range requirements.

### Installing the MIDI converter
- The MIDI converter makes use of the python library [music21](http://web.mit.edu/music21/), which must be installed in the python environment where the converter is run.
- Installation instructions for music21 on all systems, as well as python on windows can be found [here.](http://web.mit.edu/music21/doc/usersGuide/usersGuide_01_installing.html) 



## List of planned project features:

* Wiki-like website for documentation

* GUI version of MIDI converter

* Automatic client script updates

* and more!


We are not sponsored by, or affiliated with Mojang, Computercraft: Tweaked, or any of the other mentioned projects and resources.

___

## Helpful Resources

* [Computercraft: Tweaked Wiki](https://tweaked.cc/)

* [Computercraft Speaker Information](https://tweaked.cc/peripheral/speaker.html)

* [Speaker/Note Block Note Explanation](https://minecraft.fandom.com/wiki/Note_Block#Notes)

* [Free Online Virtual Piano](https://www.musicca.com/piano)

* [How to Read Music for Beginners](https://www.musicnotes.com/now/tips/how-to-read-sheet-music/)

* [musescore music notation software](https://musescore.org/en)
