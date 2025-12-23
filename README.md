# sriv-dynamictodx
### Requires Python 3.8+

This repository contains a script that creates a `default_district.xtbl` file from several tod_override files.

This file's function is similar to `timecyc.dat` from the Grand Theft Auto 3D Era series.

This file can only describe one weather condition with a half-hour period (max 48 keyframes).

You can take the file from the `tod_example` directory and make your own tod_override files and put it in the `tod_overrides` directory for further use by the script.

The files located in the `tod_overrides` directory should describe different times of the day such as morning, afternoon, evening and night.
Each such file must have a `time` field and it must be unique.

The `time` value must be float. Example:
- 7.0 = 7:00AM
- 16.5 = 4:30PM

Run the `main.py`. After the script is running, the `default_district.xtbl` file located in the `output` directory will be generated. This file will combine all your tod_override files.

You might also want to edit the `default_global.xtbl` file to correctly display the sun and moon and determine when street lighting will be turned on or off (`day_begin`, `day_end`, `tod_segments`).

# Installation
Place generated default_district.xtbl file in the game directory.

You will also need to enable dynamic tod in the game itself.

SRTT: Use the [Zolika menu](https://zolika1351.pages.dev/mods/sr3menu)

SRIV (legacy): Use the script from the [`game_script`](/game_script) directory

SRIV (ree): Use [MixFix](https://www.saintsrowmods.com/forum/threads/21923/) (__Not tested.__)
