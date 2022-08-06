-- require decoder script
local d = require "decoder"

local modem = peripheral.find("modem")
local speaker = peripheral.find("speaker")
modem.open(89)
print("Client Started")


while true do
  -- Wait for a message to arrive...
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  print("Playing "..message[1],"at tempo multiplier"..message[3])
  
  -- Play the encoded message
  for i,v in ipairs(message[2]) do

    -- find corresponding mc note number using decoder module
    -- v[3] is string version of note from song file
    -- new from McDonalds it's the mcNote!
    local mcNote = d.findNote(v[3])

    --play song note
    speaker.playNote(v[1], v[2], mcNote)

    --pause after note controlled by tempo multiplier
    sleep(v[4] * message[3])
  end
end
  
