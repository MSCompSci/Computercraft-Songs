local M = {}
-- Minecraft notes run from 0 - 24 but lua arrays are 1 indexed
noteArray = {} 
noteArray[1] = {"F#1", "Gb1"}
noteArray[2] = {"G1"}
noteArray[3] = {"G#1", "Ab1"}
noteArray[4] = {"A1"}
noteArray[5] = {"A#1", "Bb1"}
noteArray[6] = {"B1"}
noteArray[7] = {"C1"}
noteArray[8] = {"C#1", "Db1"}
noteArray[9] = {"D1"}
noteArray[10] = {"D#1", "Eb1"}
noteArray[11] = {"E1"}
noteArray[12] = {"F1"}
noteArray[13] = {"F#2", "Gb2"}
noteArray[14] = {"G2"}
noteArray[15] = {"G#2", "Ab2"}
noteArray[16] = {"A2"}
noteArray[17] = {"A#2", "Bb2"}
noteArray[18] = {"B2"}
noteArray[19] = {"C2"}
noteArray[20] = {"C#2", "Db2"}
noteArray[21] = {"D2"}
noteArray[22] = {"D#2", "Eb2"}
noteArray[23] = {"E2"}
noteArray[24] = {"F2"}
noteArray[25] = {"F#3", "Gb3"}

--finds note in noteArray
function M.findNote (n)
  local note = n
  for key, val in ipairs(noteArray) do
    for l, no in ipairs(val) do
      --print(no)
      if (no==note) then
        return key - 1
      end
    end
  end
end

return M
