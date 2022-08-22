-- Save the selected music group to play with
-- If no group is given, ignore the group parameter in the message
local group
if #arg ~= 1 then
  group = "any"
else
  group = arg[1]
end

-- require decoder script
local d = require "decoder"
local modem = peripheral.find("modem")
local speaker = peripheral.find("speaker")
modem.open(89)
--------------------
print(os.date("%T").."> Client Started in group "..group)
--------------------

while true do
  -- Wait for a message to arrive...
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  -- Special Case: Execute shell commands given in message[2]
  if (message[1] == "$shell") and ((group == "any") or (group == message["group"])) then
    print("[!] Executing Shell Commands")
    -- Run each command in the message
    for i,v in ipairs(message[2]) do
      shell.run(v)
    end
  elseif (group == "any") or (group == message["group"]) then
    -- If nothing special is sent, just play the song received
    print(os.date("%T").."> Playing "..message[1].." at TM "..message[3])
    
    sp = 1 -- set speaker value for polyphonic songs, 1 is default

    -- Play the encoded message
    for i,v in ipairs(message[2]) do
        if v[5] == sp then

        -- find corresponding mc note number using decoder module if the track uses note notation
        -- v[3] is string version of note from song file
        -- new from McDonalds it's the mcNote!
        local mcNote
        if message[4] == true then
          mcNote = d.findNote(v[3])
        else
          mcNote = v[3]
        end

        --play song note
        speaker.playNote(v[1], v[2], mcNote)

        --pause after note controlled by tempo multiplier
        sleep(v[4] * message[3])
       end
    end
  end
end
