-- The Song you want to play
local songname = "songs/bell"
if arg[1] then
  if not fs.exists(arg[1]) then
    print(arg[1].." doesn't exist")
    exit()
  end
  songname = arg[1]
end
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
