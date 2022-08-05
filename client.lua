local modem = peripheral.find("modem")
local speaker = peripheral.find("speaker")
modem.open(89)
print("Client Started")

while true do
  -- Wait for a message to arrive...
  local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  print("Playing song")
  -- Play the encoded message
  for i,v in ipairs(message) do
    speaker.playNote(v[1], v[2], v[3])
    sleep(v[4])
  end
end
  
