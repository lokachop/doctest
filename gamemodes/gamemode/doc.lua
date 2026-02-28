ZVox = ZVox or {}

---Gets the voxel ID and voxel state at a certain position given a universe.
---@shared
---@group addonapi
---@category blocks
---@param univ universe Universe to query in
---@param x integer X position to query
---@param y integer Y position to query
---@param z integer Z position to query
---@return integer? voxelID The voxel ID at that pos, nil if the universe doesn't exist
---@return integer? voxelState The voxel state at that pos
---@example_begin Gets the block at 0, 0, 0 from the main universe.
---local univ = ZVox.AddonAPI.GetUniverseByName("main")
---local voxID, voxState = ZVox.AddonAPI.GetBlockAtPos(univ, 0, 0, 0)
---@example_end
---@example_begin Checks for a block being air.
---local univ = ZVox.AddonAPI.GetUniverseByName("main")
---local cX, cY, cZ = 1, 1, 1
---local voxID, voxState = ZVox.AddonAPI.GetBlockAtPos(univ, cX, cY, cZ)
---local airID = ZVox.AddonAPI.GetVoxelID("zvox:air")
---if voxID == airID then
---	print("The voxel at " .. cX .. ", " .. cY .. ", " .. cZ .. " is air!")
---end
---@example_end
function ZVox.AddonAPI.GetBlockAtPos(univ, x, y, z)
	print("Do something...")
	print("Bleh.")
	print("Please work?...")
	print("Please?...")
	print("Final one, hopefully?")
end

---Performs a raycast on a given universe.
---@shared
---@group addonapi
---@category blocks
---@param univ universe Universe to raycast in
---@param pos Vector Origin position
---@param dir Vector Direction to raycast in, must be normalized
---@param steps integer How many steps shall we take at most
---@param killOOB boolean Whether to kill raycasts that are out of bounds or not
---@param groupMask integer Mask of what we can hit
---@return TraceResult? ret Raycast result, nil if missing any of the arguments
function ZVox.AddonAPI.RaycastWorld(univ, pos, dir, steps, killOOB, groupMask)
end