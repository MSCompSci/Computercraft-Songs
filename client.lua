-- require decoder script
local d = require "decoder"

local modem = peripheral.find("modem")
local speaker = peripheral.find("speaker")
modem.open(89)
print("Client Started")


while true do
  -- Wait for a message to arrive...
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  -- Special Case: Execute shell commands given in message[2]
  if message[1] == "$shell" then
    print("[!] Executing Shell Commands")
    -- Run each command in the message
    for i,v in ipairs(message[2]) do
      shell.run(v)
    end
  else
    -- If nothing special is sent, just play the song received
    print("[!] Playing "..message[1].." at Tempo Multiplier "..message[3])

    -- Play the encoded message
    for i,v in ipairs(message[2]) do

      -- find corresponding mc note number using decoder module if the track uses note notation
      -- v[3] is string version of note from song file
      -- new from McDonalds it's the mcNote!
      if v[4] then
        local mcNote = d.findNote(v[3])
      else
        local mcNote = v[3]
      end

      --play song note
      speaker.playNote(v[1], v[2], mcNote)

      --pause after note controlled by tempo multiplier
      sleep(v[4] * message[3])
    end
  end
end
  
