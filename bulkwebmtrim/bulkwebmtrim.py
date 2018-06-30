import sys
import os
import csv
import configparser
import glob
from pathlib import Path
from ffmpy import FFmpeg
from colorama import init, Fore


init()

config_path = Path('config.ini')
Config = configparser.ConfigParser()
if not config_path.is_file():
    config_file = open(config_path, 'w+')

    Config.add_section('Paths')
    Config.set('Paths', 'OutputDir', 'W:\\WEBM\\')

    Config.add_section('CSV')
    Config.set('CSV', 'Delimiter', '$')

    Config.add_section('Encoding')
    Config.set('Encoding', '4chan Filesize Limit', 'False')

    Config.write(config_file)
    config_file.close()

Config.read(config_path)
output_dir = Config['Paths']['OutputDir']
csv_delimiter = Config['CSV']['Delimiter']




for in_path in sys.argv[1:]:
    in_path = Path(in_path).resolve()

    if os.path.isfile(in_path) and ((in_path.suffix == '.csv') or (in_path.suffix == '.txt')):
        index = 1
        filename = in_path.stem

        if not os.path.exists(output_dir + filename):
            os.makedirs(output_dir + filename)


        with open(in_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=csv_delimiter)


            for row in readCSV:
                for file_result in glob.glob(str(in_path).split('.')[0] + '*'):
                    if not file_result.endswith('.csv') and not file_result.endswith('.txt'):
                        input_file = Path(file_result)
                        break


                output_filename = "{:02} ".format(index) + filename + ' ' + row[2] + '.webm'
                output_arg = '-c:v libvpx-vp9 -pix_fmt yuv420p -threads 8 -slices 4 -ac 2 -c:a libopus -qmin 28 -crf 30 -qmax 32 -qcomp 1 -b:v 0 -b:a 128000 -vbr on -f webm'

                start_h = int(row[0][0:2])
                start_m = int(row[0][2:4])
                start_s = int(row[0][4:6])
                start = start_s + (start_m * 60) + (start_h * 60 * 60)

                if row[1] != 'end':
                    stop_h = int(row[1][0:2])
                    stop_m = int(row[1][2:4])
                    stop_s = int(row[1][4:6])
                    stop = stop_s + (stop_m * 60) + (stop_h * 60 * 60)
                    input_arg = '-ss {} -to {}'.format(start, stop)

                else:
                    stop_h = 99
                    stop_m = 99
                    stop_s = 99
                    input_arg = '-ss {}'.format(start)


                try:
                    if row[3] == '+':
                        output_arg += ' -vf transpose=clock'
                    elif row[3] == '-':
                        output_arg += ' -vf transpose=cclock'
                except IndexError:
                    pass


                ff = FFmpeg(
                    inputs={str(input_file): input_arg},
                    outputs={output_dir + filename + '\\' + output_filename: output_arg}
                )

                print('Filename: ' + Fore.YELLOW + output_filename + Fore.RESET +
                      '\nFrom ' + Fore.MAGENTA + '{:02}:{:02}:{:02}'.format(start_h, start_m, start_s) + Fore.RESET +
                      ' to ' + Fore.MAGENTA + '{:02}:{:02}:{:02}'.format(stop_h, stop_m, stop_s) + Fore.RESET +
                      '\n\nRunning command:\n' + Fore.CYAN + ff.cmd + Fore.RESET)
                ff.run()
                print(Fore.GREEN + '\nCONVERSION COMPLETED\n\n\n' + Fore.RESET)

                index += 1
    else:
        print(Fore.RED + '"{}" is not a supported filetype'.format(str(in_path)) + Fore.RESET)
