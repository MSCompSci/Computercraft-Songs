-- The Song you want to play
local songname = "songs/bell"
require songname

local modem = peripheral.find("modem")
print("Server Started")

while true do
  -- Wait for a message to arrive...
  -- local event, modemSide, senderChannel, replyChannel, message, senderDistance = os.pullEvent("modem_message")
  os.pullEvent("redstone")
  if rs.getInput("right") do
      modem.transmit(89, 1, song)
      print("Sending "..songname)
      sleep(1)
  end
end
