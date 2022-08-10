-- The Song you want to play
-- local songname = "songs/bell"
if #arg ~= 2 then
  print("Usage: server <songfile> <group>")
  return
end
-- Ensure the song file exists
if not fs.exists(arg[1]..".lua") then
  print(arg[1].." doesn't exist")
  return
end
songname = arg[1]

-- Grab the message object from the song file
require(songname)
-- Append the group to send the song to
message["group"] = arg[2]

local modem = peripheral.find("modem")
print(os.date("%T").."> Server Started with song "..songname.." and group "..message["group"])

while true do
  -- Wait for a redstone signal from the right...
  os.pullEvent("redstone")
  if rs.getInput("right") then
      modem.transmit(89, 1, message)
      print(os.date("%T").."> Sending "..songname)
      sleep(0.5)
  end
end
