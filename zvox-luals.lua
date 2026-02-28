---@meta

ZVox = ZVox or {}
ZVox.AddonAPI = ZVox.AddonAPI or {}

---@alias universe table Universe object
---@alias worldgenerator table

---Gets the voxel ID and voxel state at a certain position given a universe.
---@shared
---@param univ universe Universe to query in
---@param x integer X position to query
---@param y integer Y position to query
---@param z integer Z position to query
---@return integer? voxelID The voxel ID at that pos, nil if the universe doesn't exist
---@return integer? voxelState The voxel state at that pos
function ZVox.AddonAPI.GetBlockAtPos(univ, x, y, z) end
---Performs a raycast on a given universe.
---@shared
---@param univ universe Universe to raycast in
---@param pos Vector Origin position
---@param dir Vector Direction to raycast in, must be normalized
---@param steps integer How many steps shall we take at most
---@param killOOB boolean Whether to kill raycasts that are out of bounds or not
---@param groupMask integer Mask of what we can hit
---@return TraceResult? ret Raycast result, nil if missing any of the arguments
function ZVox.AddonAPI.RaycastWorld(univ, pos, dir, steps, killOOB, groupMask) end
---Gets the icon material for a texturepack
---@client
---@internal
---@return IMaterial icon The icon
function ZVox.GetTexturePackIconMat() end
---Does something
---@shared
---@internal
---@param var number A parameter!
---@return number num A number
function ZVox.DoSomething(var) end
