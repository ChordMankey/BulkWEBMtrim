import sys
import os
import csv
from ffmpy import FFmpeg


filename = os.path.basename(sys.argv[1]).split('.')[0]

if not os.path.exists('W:\\WEBM\\' + filename):
    os.makedirs('W:\\WEBM\\' + filename)


index = 1
with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter='$')


    for row in readCSV:
        output_filename = "{:02} ".format(index) + filename + ' ' + row[2] + '.webm'

        start_h = int(row[0][0:2])
        start_m = int(row[0][2:4])
        start_s = int(row[0][4:6])
        start = str( start_s + (start_m * 60) + (start_h * 60 * 60) )

        if row[1] != 'end':
            stop_h = int(row[1][0:2])
            stop_m = int(row[1][2:4])
            stop_s = int(row[1][4:6])
            stop = str( stop_s + (stop_m * 60) + (stop_h * 60 * 60) )

            ff = FFmpeg(
                # global_options='-v quiet -stats',

                inputs={sys.argv[1].split('.')[0] + '.mp4': ['-ss', start,
                                                             '-to', stop
                                                             ]},

                outputs={'W:\\WEBM\\' + filename + '\\' + output_filename: ['-c:v', 'libvpx-vp9',
                                                                            '-pix_fmt', 'yuv420p',
                                                                            '-threads', '8',
                                                                            '-slices', '4',
                                                                            '-ac', '2',
                                                                            '-c:a', 'libopus',
                                                                            # '-c:a', 'libvorbis',
                                                                            '-qmin', '28',
                                                                            '-crf', '30',
                                                                            '-qmax', '32',
                                                                            '-qcomp', '1',
                                                                            '-b:v', '0',
                                                                            '-b:a', '128000',
                                                                            '-vbr', 'on',
                                                                            # '-qscale:a', '3',
                                                                            '-f', 'webm'
                                                                            ]}
            )

        else:
            ff = FFmpeg(
                # global_options='-v quiet -stats',

                inputs={sys.argv[1].split('.')[0] + '.mp4': ['-ss', start
                                                             ]},

                outputs={'W:\\WEBM\\' + filename + '\\' + output_filename: ['-c:v', 'libvpx-vp9',
                                                                            '-pix_fmt', 'yuv420p',
                                                                            '-threads', '8',
                                                                            '-slices', '4',
                                                                            '-ac', '2',
                                                                            '-c:a', 'libopus',
                                                                            # '-c:a', 'libvorbis',
                                                                            '-qmin', '28',
                                                                            '-crf', '30',
                                                                            '-qmax', '32',
                                                                            '-qcomp', '1',
                                                                            '-b:v', '0',
                                                                            '-b:a', '128000',
                                                                            '-vbr', 'on',
                                                                            # '-qscale:a', '3',
                                                                            '-f', 'webm'
                                                                            ]}
            )



        ff.run()
        index+=1