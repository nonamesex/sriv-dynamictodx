from io import StringIO
from os import makedirs, path
from xml.dom.minidom import parse

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

def time_from_military(time: str) -> tuple[int, int]:
	hour = int(time) / 100
	minute = (hour - int(hour)) * 60
	return (int(hour), int(minute))

def time_to_military(time: float):
	hour = int(time)
	minute = int((time - hour) * 60)
	return f"{hour:02d}{minute:02d}"

def read_tod_district(tod_path: str) -> dict[str, dict[str, str]]:
	tod_params = {}

	with parse(tod_path) as tod_xml:
		for param_name in TOD_PARAMS:
			elements = tod_xml.getElementsByTagName(param_name)
			if elements.length == 0:
				continue

			keys = elements[0].getElementsByTagName("key")

			for key in keys:
				time = key.getElementsByTagName("time")[0].childNodes[0].wholeText # type: ignore
				value = key.getElementsByTagName("value")[0].childNodes[0].wholeText # type: ignore

				time = str(int(time) / 2)

				if time not in tod_params:
					tod_params[time] = {}

				tod_params[time][param_name] = value

	return tod_params

def write_tod_override(tod_params: dict[str, str], time: str, mission_name = "unnamed"):
	time_military = time_to_military(float(time))

	output_path = path.join(SCRIPT_DIR, "output", f"{time_military}_{mission_name}.xtbl")
	output_dir = path.dirname(output_path)

	if not path.exists(output_dir):
		makedirs(output_dir, exist_ok = True)

	with StringIO() as result:
		result.write("<root>\n\t<Table>\n\t\t<mission_override>\n")
		result.write(f"\t\t\t<mission_name>{mission_name}</mission_name>\n")
		result.write(f"\t\t\t<time>{time}</time>\n")

		for param_name, param_value in tod_params.items():
			result.write(f"\t\t\t<{param_name}>{param_value}</{param_name}>\n")

		result.write("\t\t</mission_override>\n\t</Table>\n</root>\n")

		with open(output_path, "wt", encoding = "utf_8") as output:
			output.write(result.getvalue())

def main():
	district_path = path.join(SCRIPT_DIR, "default_district.xtbl")
	district_params = read_tod_district(district_path)
	mission_name = path.splitext(path.basename(district_path))[0]

	for time, params in district_params.items():
		write_tod_override(params, time, mission_name)

if __name__ == "__main__":
	main()
