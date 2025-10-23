-- This script must be loaded via sr3_city.lua using the include function
-- and then calling the dynamic_tod_main function in the sr3_city_main function

local function dynamic_tod_can_be_enabled()
	if mission_is_active() then
		return false
	end

	if not mission_is_complete("m03") then
		return false
	end

	return true
end

local function enable_dynamic_tod(first_time)
	if dynamic_tod_can_be_enabled() then
		dynamic_tod_enable(true)

		if not not first_time then
			local tod_segments = { 5.0, 9.5, 14.5, 21.0 }
			local tod_segment = tod_segments[rand_int(1, #tod_segments)]
			local hour = floor(tod_segment)
			local minute = floor((tod_segment - hour) * 60)
			set_time_of_day(hour, minute)
		end
	end
end

local function on_mission_start()
	dynamic_tod_enable(false)
end

local function on_mission_end()
	enable_dynamic_tod()
end

local IS_ANY_MISSION_ACTIVE = false
function dynamic_tod_thread()
	dynamic_tod_enable(false)
	enable_dynamic_tod(true)

	while true do
		if mission_is_active() and not IS_ANY_MISSION_ACTIVE then
			IS_ANY_MISSION_ACTIVE = true
			on_mission_start()
		elseif not mission_is_active() and IS_ANY_MISSION_ACTIVE then
			IS_ANY_MISSION_ACTIVE = false
			on_mission_end()
		end
		thread_yield()
	end
end

function dynamic_tod_main()
	thread_new("dynamic_tod_thread")
end
