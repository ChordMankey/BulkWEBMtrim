import sys
import os
import csv
from ffmpy import FFmpeg


for in_path in sys.argv[1:]:
    if os.path.isfile(in_path):
        index = 1
        filename = os.path.basename(in_path).split('.')[0]

        if not os.path.exists('W:\\WEBM\\' + filename):
            os.makedirs('W:\\WEBM\\' + filename)


        with open(in_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter='$')


            for row in readCSV:
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
                    input_arg = '-ss {}'.format(start)


                try:
                    if row[3] == '+':
                        output_arg += ' -vf transpose=clock'
                    elif row[3] == '-':
                        output_arg += ' -vf transpose=cclock'
                except IndexError:
                    pass


                ff = FFmpeg(
                    inputs={in_path.split('.')[0] + '.mp4': input_arg},
                    outputs={'W:\\WEBM\\' + filename + '\\' + output_filename: output_arg}
                )


                ff.run()
                index+=1