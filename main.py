from io import StringIO
from math import floor
from os import listdir, makedirs, path
from xml.dom.minidom import parse

INCLUDE_SR4_DEFAULTS = False
"""Apply default_district SR4 params over SR3 base ones?"""

COMPACT_KEY_OUTPUT = False
"""Output one key per line?"""

SCRIPT_DIR = path.dirname(__file__)
TOD_PARAMS = [
	"ambient_audio_rtpc",
	"ambient_color",
	"back_ambient_color",
	"bloom_amount",
	"bloom_exposure",
	"bloom_slope_A",
	"bloom_slope_B",
	"bloom_theta",
	"brightpass_offset_new",
	"brightpass_threshold_new",
	"cloud_backlight_power",
	"cloud_backlight_strength",
	"cloud_layer01_speed",
	"cloud_layer23_speed",
	"clouds_front_light_color",
	"clouds_horizon_front_light_color",
	"clouds_horizon_rear_light_color",
	"clouds_rear_light_color",
	"desired_brightness",
	"dof_blur_radius",
	"dof_far",
	"dof_near",
	"east0",
	"east1",
	"east2",
	"east3",
	"exposure_max",
	"exposure_min",
	"eye_adaption_amount",
	"eye_adaption_base",
	"eye_fade_max",
	"eye_fade_min",
	"film_grain_amount",
	"film_grain_saturation",
	"fog_atmosphere_scale",
	"fog_color",
	"fog_density_new",
	"fog_density_offset",
	"fog_ground",
	"ground_reflection_brightness",
	"ground_reflection_gloss",
	"ground_reflection_spec_refl_brightness",
	"horizon_layer0_strength",
	"horizon_layer1_strength",
	"horizon_layer2_strength",
	"horizon_layer3_strength",
	"horizon_mountain_color_back",
	"horizon_mountain_color",
	"horizon_mountain_fog_color",
	"horizon_mountain_fog_density",
	"horizon_mountain_normal_map_height",
	"horizon_storm_strength",
	"iris_rate",
	"ldr_max",
	"ldr_min",
	"luminance_mask_max",
	"luminance_max",
	"luminance_min",
	"lut_filename",
	"meteor_strength",
	"overhead_layer0_strength",
	"overhead_layer1_strength",
	"overhead_layer2_strength",
	"overhead_layer3_strength",
	"overhead_storm_strength",
	"particle_ambient_color",
	"particle_tod_light_color",
	"star_strength",
	"tod_light_color",
	"tonemap_lum_offset",
	"tonemap_lum_range",
	"vignette_amount",
	"vignette_curve",
	"water_ambient_color",
	"water_crest_color",
	"water_crest_threshold",
	"water_diffuse_color1",
	"water_diffuse_color2",
	"water_falloff_color",
	"water_fog_color",
	"water_specular_alpha",
	"water_specular_color",
	"water_specular_power",
	"west0",
	"west1",
	"west2",
	"west3",
	"window_color",
	"zenith",

	# tod override
	"time"
]

KEYS_PER_HOUR = 2
KEYS_NUM = 24 * KEYS_PER_HOUR
def get_key_from_time(time: float) -> int:
	key = int(time * KEYS_PER_HOUR)

	if key >= KEYS_NUM:
		key = key % KEYS_NUM
	elif 0 > key:
		key = KEYS_NUM + key

	return key

def read_tod(tod_path: str, is_tod_override = False) -> dict[str, str]:
	if not path.exists(tod_path) or not path.isfile(tod_path):
		return {}

	tod_params = {}

	with parse(tod_path) as tod_xml:
		if is_tod_override:
			elements = tod_xml.getElementsByTagName("mission_override")
			if elements.length == 0:
				return tod_params

			tod_xml = elements[0]

		for param_name in TOD_PARAMS:
			elements = tod_xml.getElementsByTagName(param_name)
			if elements.length == 0:
				continue

			element = elements[0]
			if element.childNodes.length == 0:
				continue

			value = element.childNodes[0].wholeText # type: ignore
			if value and value != "":
				tod_params[param_name] = value

	return tod_params

def get_default_tod_params() -> dict[str, str]:
	default_params = {}

	district_files = [
		"sr3_base_district.xml"
	]

	if INCLUDE_SR4_DEFAULTS:
		district_files.append("sr4_default_district.xml")

	for tod_file in district_files:
		tod_path = path.join(SCRIPT_DIR, "tod_defaults", tod_file)
		tod_params = read_tod(tod_path, is_tod_override = False)
		default_params = {**default_params, **tod_params}

	return default_params

def tod_district_build() -> dict[str, str]:
	tod_overrides_dir = path.join(SCRIPT_DIR, "tod_overrides")
	default_params = get_default_tod_params()
	tods_params = []

	for tod_filename in listdir(tod_overrides_dir):
		if not tod_filename.endswith(".todx") and not tod_filename.endswith(".xtbl"):
			continue

		tod_path = path.join(tod_overrides_dir, tod_filename)
		tod_params = read_tod(tod_path, is_tod_override = True)
		tods_params.append(tod_params)

	sorted(tods_params, key = lambda tod_params: tod_params["time"])

	tod_district = {}

	for tod_params in tods_params:
		key = get_key_from_time(float(tod_params["time"]))

		for param_name in TOD_PARAMS:
			if param_name == "time":
				continue

			if param_name not in tod_district:
				tod_district[param_name] = []

			if param_name in tod_params:
				tod_district[param_name].append([key, tod_params[param_name]])
			else:
				tod_district[param_name].append([key, default_params[param_name]])

	return tod_district

def tod_district_write(tod_district: dict[str, str]):
	output_path = path.join(SCRIPT_DIR, "output", "default_district.xtbl")
	output_dir = path.dirname(output_path)

	if not path.exists(output_dir):
		makedirs(output_dir, exist_ok = True)

	with StringIO() as result:
		result.write("<root>\n")

		for param_name, param_value in tod_district.items():
			result.write(f"\t<{param_name}>\n")

			for key, value in param_value:
				if COMPACT_KEY_OUTPUT:
					result.write(f"\t\t<key><time>{key}</time><value>{value}</value></key>\n")
				else:
					result.write(f"\t\t<key>\n\t\t\t<time>{key}</time>\n\t\t\t<value>{value}</value>\n\t\t</key>\n")

			result.write(f"\t</{param_name}>\n")

		result.write("</root>\n")

		with open(output_path, "wt", encoding = "utf_8") as output:
			output.write(result.getvalue())

def main():
	tod_district = tod_district_build()
	tod_district_write(tod_district)

if __name__ == "__main__":
	main()
