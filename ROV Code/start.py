import configparser
import control
import camera
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Red Sea ROV Controller V3")
	parser.add_argument("-c", "--show_camera", required=False, action="store_true", help="Share camera from ROV to computer screen")
	parser.add_argument("-rc", "--record_camera", required=False, action="store_true", help="Record input on the camera into an mp4 file")
	parser.add_argument("-s", "--show_sterioscope", required=False, action="store_true", help="Share sterioscopic camera from ROV to computer screen")
	parser.add_argument("-m", "--sterioscope_model", required=False, action="store_true", help="Create 3D model from sterioscopic camera perspectives and computer vision")
	parser.add_argument("-k", "--keyboard_input", required=False, action="store_true", help="Use keyboard to send input to ROV")
	parser.add_argument("-c", "--controller_input", required=False, action="store_true", help="Use controller to send input to ROV")
	# parser.add_argument("-c", "--disable_camera", required=False, action="store_true", help="Start the controller without starting the camera feed")
	# parser.add_argument("-z", "--override_warnings", required=False, action="store_true", help="Automatically override warnings, like the LEAK warning")
	# parser.add_argument("-f", "--fake_thrusters", required=False, action="store_true", help="Start the controller without actually connecting to the thrusters")
	# parser.add_argument("-g", "--fake_sensors", required=False, action="store_true", help="Start the controller with a fake sensors implementation")
	args = parser.parse_args()
	
	config = configparser.ConfigParser()
	config.read("config.ini")
	
	print("")

	control.init(config)#, args.override_warnings, args.fake_thrusters, args.fake_sensors)
	#camera.kill(process, raspiProcess)