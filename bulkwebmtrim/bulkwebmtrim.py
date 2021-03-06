import sys
import os
import csv
import configparser
import glob
from pathlib import Path
from ffmpy import FFmpeg
from colorama import init, Fore


def convert_video(input_file, input_arg, output_file, output_arg):
    ff = FFmpeg(
        inputs={str(input_file): input_arg},
        outputs={str(output_file): output_arg}
    )

    print('Filename: ' + Fore.YELLOW + Path(output_file).name + Fore.RESET +
          '\nFrom ' + Fore.MAGENTA + '{:02}:{:02}:{:02}'.format(start[0], start[1],
                                                                start[2]) + Fore.RESET +
          ' to ' + Fore.MAGENTA + '{:02}:{:02}:{:02}'.format(stop[0], stop[1], stop[2]) + Fore.RESET +
          '\n\nRunning command:\n' + Fore.CYAN + ff.cmd + Fore.RESET)

    os.environ['FFREPORT'] = 'file=' + output_file.stem + '.log' + ':level=32'
    ff.run()
    del os.environ['FFREPORT']


def row_parse(row, index, input_file, out_dir):
    filename = input_file.stem
    input_arg = ''
    output_arg = '-c:v libvpx-vp9 -pix_fmt yuv420p -threads 8 -slices 4 -ac 2 -c:a libopus -qmin 28 -crf 30 -qmax 32 -qcomp 1 -b:v 0 -b:a 128000 -vbr on -f webm -loglevel error'

    global start
    global stop

    if '|' in row[0]:
        # https://stackoverflow.com/questions/50594412/cut-multiple-parts-of-a-video-with-ffmpeg
        id_char = 'a'
        multi_index = 0
        vf = ''
        af = ''
        vf += """-vf "select='"""
        af += """-af "aselect='"""

        for times in row:
            if '|' in times:
                start_str = times.split('|')[0]
                stop_str = times.split('|')[1]

                start = [None] * 10
                start[0] = int(start_str[0:2])
                start[1] = int(start_str[2:4])
                start[2] = int(start_str[4:6])
                start_time = start[2] + (start[1] * 60) + (start[0] * 60 * 60)

                stop = [None] * 10
                if stop_str != 'end':
                    stop[0] = int(stop_str[0:2])
                    stop[1] = int(stop_str[2:4])
                    stop[2] = int(stop_str[4:6])
                    stop_time = stop[2] + (stop[1] * 60) + (stop[0] * 60 * 60)

                    vf += 'between(t,{},{})+'.format(start_time, stop_time)
                    af += 'between(t,{},{})+'.format(start_time, stop_time)

                else:
                    stop[0] = 99
                    stop[1] = 99
                    stop[2] = 99

                    vf += 'gte(t,{})+'.format(start_time)
                    af += 'gte(t,{})+'.format(start_time)

                    
                multi_index += 1

            else:
                vf = vf[:-1] + "',setpts=N/FRAME_RATE/TB"
                af = af[:-1] + "',asetpts=N/SR/TB" + '"'
                break

        output_filename = "{:02} ".format(index) + filename + ' ' + row[multi_index] + '.webm'
        multi_index += 1

        try:
            if row[multi_index] == '+':
                vf += ',transpose=clock"'
            elif row[multi_index] == '-':
                vf += ',transpose=cclock"'
            else:
                vf += '"'
        except IndexError:
            vf += '"'

        output_arg += ' {} {}'.format(vf, af)

    else:
        output_filename = "{:02} ".format(index) + filename + ' ' + row[2] + '.webm'

        start = [None] * 10
        start[0] = int(row[0][0:2])
        start[1] = int(row[0][2:4])
        start[2] = int(row[0][4:6])
        start_time = start[2] + (start[1] * 60) + (start[0] * 60 * 60)

        stop = [None] * 10
        if row[1] != 'end':
            stop[0] = int(row[1][0:2])
            stop[1] = int(row[1][2:4])
            stop[2] = int(row[1][4:6])
            stop_time = stop[2] + (stop[1] * 60) + (stop[0] * 60 * 60)
            input_arg = '-ss {} -to {}'.format(start_time, stop_time)

        else:
            stop[0] = 99
            stop[1] = 99
            stop[2] = 99
            input_arg = '-ss {}'.format(start_time)

        try:
            if row[3] == '+':
                output_arg += ' -vf transpose=clock'
            elif row[3] == '-':
                output_arg += ' -vf transpose=cclock'
        except IndexError:
            pass


    output_file = out_dir.joinpath(output_filename) # Path(config['OutputDir'] + filename + '\\' + output_filename)
    try:
        convert_video(input_file, input_arg, output_file, output_arg)
    except Exception as e:
        print(Fore.RED + '\nCONVERSION FAILED:\n' + Fore.CYAN + str(e) + '\n\n\n' + Fore.RESET)
    else:
        print(Fore.GREEN + '\nCONVERSION COMPLETED\n\n\n' + Fore.RESET)



def csv_parse(in_path, out_dir):
    in_path = Path(in_path)

    input_file = None
    for file_result in glob.glob(str(in_path).split('.')[0] + '*'):
        if not file_result.endswith('.csv') and not file_result.endswith('.txt'):
            input_file = Path(file_result)
            break

    with open(in_path) as csvfile:
        index = 1  # Index for output filenames
        read_csv = csv.reader(csvfile, delimiter=config['Delimiter'])

        for row in read_csv:
            row_parse(row, index, input_file, out_dir)
            index += 1





def configuration(config_path):
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str

    if not config_path.is_file():
        config_file = open(config_path, 'w+')

        config_parser.add_section('Paths')
        config_parser.set('Paths', 'OutputDir', 'W:\\WEBM\\')

        config_parser.add_section('CSV')
        config_parser.set('CSV', 'Delimiter', '$')

        config_parser.add_section('Encoding')
        config_parser.set('Encoding', '4chan Filesize Limit', 'False')

        config_parser.write(config_file)
        config_file.close()

    config_parser.read(config_path)
    config = {}
    config.update(config_parser['Paths'])
    config.update(config_parser['CSV'])

    return config


def traverser(master_path):
    # Checks each argument excluding the first one and only processes
    # files with extension .txt or .csv
    for in_path in master_path:
        in_path = Path(in_path).resolve()

        if os.path.isfile(in_path) and ((in_path.suffix == '.csv') or (in_path.suffix == '.txt')):
            filename = in_path.stem
            parent = in_path.parts[-2]
            out_dir = Path(config['OutputDir']).joinpath(parent, filename)

            out_dir.mkdir(parents=True, exist_ok=True)

            csv_parse(in_path, out_dir)

        elif os.path.isdir(in_path):
            traverser(in_path.iterdir())

        else:
            print(Fore.RED + '"{}" is not a supported filetype'.format(str(in_path)) + Fore.RESET)



def main():
    # Initialises colorama to support coloured stdout
    # printing on Windows.
    init()

    traverser(sys.argv[1:])


# Creates config.ini file if it doesn't exist and sets default options,
# then proceeds to parse config file in-case it already exists.
config_path = Path('config.ini')
config = configuration(config_path)

if __name__ == '__main__':
    main()
