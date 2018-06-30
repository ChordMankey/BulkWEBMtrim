# BulkWEBMtrim

BulkWEBMtrim allows you to quickly trim multiple sections from video files into webm files using a csv file to mention the starting and ending points.

## Getting Started

### Prerequisites

At the moment I haven't prepared any binaries so you need to run `bulkwebmtrim.py` from source. Therefore you need these libraries installed:
* ffmpy - Python wrapper for ffmpeg which is used for video conversion
* colorama - For the nice and colourful console output

Python 3 is required.

The commands below will get the required libraries installed through pip.
```
pip install ffmpy
pip install colorama
```

### Installing

Download `bulkwebmtrim.py` from source and run it, I haven't prepared binaries yet sadly.

### Usage

Create a csv or text file with the same filename as your video (the input video can be of pretty much any format) and place it in the same directory as your video.
So if your video file is `my_video.mkv`, your csv file should be `my_video.csv` or `my_video.txt`.

Format your csv file as follows (The top row is not needed of course):

| Start Time  | Stop Time | Filename Appendage | Rotation |
| ----------- | --------- | ------------------ | -------- |
| hhmmss | hhmmss or 'end' | text | + or - |

* + = 90 Degrees Clockwise
* - = 90 Degrees Anti-Clockwise

Examples:

| Start Time  | Stop Time | Filename Appendage | Rotation |
| ----------- | --------- | ------------------ | -------- |
| 000000 | 001510 | favourite part | |
| 002708 | end | other part | |

Keep in mind that the default csv delimiter in my program is '$' (this can be changed using the config.ini file created at runtime, or created manually) so the file content will look like this:  
000000$001510$favourite part  
002708$end$other part


For a video titled `my_video.mkv` and `my_video.csv` with the content shown above, the outputs will be:
* `my_video favourite part.webm` From 00:00:00 to 00:15:10
* `my_video other part.webm` From 00:27:08 to the end of the video


Once you've got the csv file(s) ready, execute `bulkwebmtrim.py` with the csv files as arguments, relative paths and absolute paths are both fine.

I've got the path to `bulkwebmtrim.py` in my PATH environment variable so I can run it directly from the terminal. So I open a terminal in my folder of videos and execute like so:
```
bulkwebmtrim.py my_video_1.csv my_video_2.csv
```

Your video output directory and csv file delimiter can be set by creating a `config.ini` file like shown below:
```
[Paths]
outputdir = W:\WEBM\

[CSV]
delimiter = $
```

The config above is the default config created when you first run the program (if a `config.ini` file doesn't exist) and most people won't have a path `W:\WEBM\` so the program will fail on first run if the config file doesn't exist.

## Authors

* **ChordMankey**

## License

I don't know much about license stuff yet but I request that you credit me and link to my project page if you use my code for anything, thanks in advance!

