import configparser
import control
import argparse
from pathlib import Path

if __name__ == "__main__":
    # TODO: utilize these arguments
    parser = argparse.ArgumentParser(description="Red Sea ROV Controller V3")
    parser.add_argument("-sc", "--show_camera_seperate", required=False, action="store_true", help="Share camera from ROV to computer screen as a seperate window")
    parser.add_argument("-s", "--show_sterioscope", required=False, action="store_true", help="Share sterioscopic camera from ROV to computer screen")
    parser.add_argument("-m", "--sterioscope_model", required=False, action="store_true", help="Create 3D model from sterioscopic camera perspectives and computer vision")
    parser.add_argument("-c", "--controller_input", required=False, action="store_true", help="Use controller to send input to ROV")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    
    read_files = config.read(str(Path(__file__).parent/"sett.ini"))  # Get sett.ini as a child of the shared parent directory, using wierd pathlib commands

    print("\n\n\n\n\n\n\n\n\n\n")

    control.init(config)#, args.override_warnings, args.fake_thrusters, args.fake_sensors)
    control.loop()