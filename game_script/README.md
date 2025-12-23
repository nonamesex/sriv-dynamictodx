# game_script
This script enables or disables dynamic tod when the player completes or starts a mission.

This script uses the `dynamic_tod_enable` function, which is only available in `sriv_legacy`. It is not possible to work in other SR games/versions.

You need to put the `dynamic_tod.lua` file in the game directory and then include the script in `sr3_city.lua` for the script to work.

First, you include the script by writing the line `include("dynamic_tod.lua")` at the beginning of the file.
Example:
```diff
+include("dynamic_tod.lua")
+
\--SR3 City Lua file
...
```

And then you add the `dynamic_tod_main` function call to the `sr3_city_main` function.
Example:
```diff
...
end

function sr3_city_main()
+	dynamic_tod_main()
end

function sr3_city_init_client()
...
```
