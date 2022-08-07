-- The Song you want to play
local songname = "songs/bell"
if arg[1] then
  if not fs.exists(arg[1]..".lua") then
    print(arg[1].." doesn't exist")
    exit()
  end
  songname = arg[1]
end
require(songname)

local modem = peripheral.find("modem")
print("Server Started with song: "..songname)

while true do
  -- Wait for a message to arrive...
  os.pullEvent("redstone")
  if rs.getInput("right") then
      modem.transmit(89, 1, message)
      print("Sending "..songname)
      sleep(1)
  end
end
