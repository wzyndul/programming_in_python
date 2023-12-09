from simulation import Simulation
import argparse
import configparser


def validate_positive_float(value, field_name):
    try:
        float_value = float(value)
        if float_value <= 0:
            raise ValueError(f"{field_name} must be a positive number.")
        return float_value
    except ValueError:
        raise ValueError(f"{field_name} must be a valid positive number.")


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    init_pos_limit = validate_positive_float(config.get('Sheep', 'InitPosLimit'), 'InitPosLimit')
    sheep_move_dist = validate_positive_float(config.get('Sheep', 'MoveDist'), 'MoveDist')
    wolf_move_dist = validate_positive_float(config.get('Wolf', 'MoveDist'), 'MoveDist')

    return init_pos_limit, sheep_move_dist, wolf_move_dist


def validate_log_level(value):
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if value not in valid_levels:
        raise argparse.ArgumentTypeError(f"Invalid log level. Choose one of {', '.join(valid_levels)}")
    return value

def main():
    # TODO wez to potem dostosuj odpoiwdni
    custom_description = (
        "This script performs a simulation based on specified parameters. "
        "It supports configuration through command-line options and an optional INI file.\n\n"
        "Additional information about the script:\n"
        "- The simulation involves sheep and wolves moving within specified limits.\n"
        "- You can customize the simulation parameters using command-line options or a configuration file.\n"
        "- If the -h/--help option is provided, this help message will be displayed, and the simulation will not be performed."
    )
    parser = argparse.ArgumentParser(description=custom_description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str,  metavar='FILE',  help='Path to the configuration file')
    parser.add_argument('-s', '--sheep', type=int, metavar='NUM', help='Number of sheep')
    parser.add_argument('-r', '--rounds', type=int, metavar='NUM', help='Maximum number of rounds')
    parser.add_argument('-w', '--wait', action='store_true', help='Pause simulation at the end of each round')
    parser.add_argument('-l', '--log', metavar='LEVEL', type=validate_log_level,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Specify the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    args = parser.parse_args()

    if args.config:
        try:
            init_pos_limit, sheep_move_dist, wolf_move_dist = read_config(args.config)
        except Exception as e:
            print(f"Error reading configuration file: {str(e)}")
            return
    else:
        init_pos_limit = 10.0
        sheep_move_dist = 0.5
        wolf_move_dist = 1.0

    if args.sheep:
        sheep_nr = args.sheep
    else:
        sheep_nr = 15

    if args.rounds:
        rounds_nr = args.rounds
    else:
        rounds_nr = 50

    simulation = Simulation(max_round_nr=rounds_nr, sheep_nr=sheep_nr, limit=init_pos_limit,
                            sheep_move=sheep_move_dist, wolf_move=wolf_move_dist, pause=args.wait, log_level=args.log)
    simulation.start()


if __name__ == "__main__":
    main()
