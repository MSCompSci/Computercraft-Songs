-- Test song sample
track = {}
track[1] = {"bass", 3, "C1", .5}
track[2] = {"bass", 3, "D2", .125}
track[3] = {"bass", 3, "Gb2", .125}

-- song format is song name, song array, tempo multiplier, note notation usage
-- named message to emulate incoming streamed format
-- tempo multiplier: standard is 1
-- make greater than 1 for longer, less for shorter
message = {"testing_song", track, 1, true}
