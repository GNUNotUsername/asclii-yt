from os                 import linesep, listdir, mkdir, path, remove, rmdir, system
from sys                import argv
from datetime           import datetime
from hashlib            import sha256
from vlc                import MediaPlayer
from urllib.error       import URLError
from cv2                import VideoCapture, imwrite, CAP_PROP_FPS
from pytube             import YouTube
from pytube.exceptions  import AgeRestrictedError, VideoUnavailable
from PIL                import Image
from ffmpeg             import FFmpeg

from time               import sleep


# Argv
DIMS_IND        = 2
GOOD_ARGV       = 3
LINK_IND        = 1

# Art
ANSI_FN_CALL    = "\x1b["
BLOCK           = "██"
COLOUR_SEP      = ";"
SET_RGB         = "38;2;"
SGR             = "m"
WIPE_SCREEN     = "clear"

# Audio
AUDIO_FNAME     = "audio.mp3"
AUDIO_OPS       = {"codec:v": "libx264"}

# Dimensions
DIMS_DELIM      = "x"

# Error messages
AGE_RESTRICTED  = "Age restricted videos cannot be downloaded"
ALREADY_EXISTS  = "Could not create a temporary directory to extract video frames"
BAD_ARGV        = "Usage: python3 asclii-yt.py link (width)x(height)"
BAD_DIM_COUNT   = "Two numeric frame dimensions are required"
BAD_LINK        = "Invalid youtube link provided"
DOWNLOAD_FAIL   = "Video could not be downloaded"
NO_INTERNET     = "Temporary failure in name resolution"
NOT_A_LINK      = "Link provided is not a youtube video"
F_NOT_SUPPORTED = "Only MP4 videos are supported presently"

# Exit values
BAD_ARGS        = 1
BAD_VID         = 2
NOT_SUPPORTED   = 3
CANT_EXTRACT    = 4

# Pathing
HIDDEN          = "."
STR_ENCODING    = "utf-8"

# File Extensions
EXTENSION_DELIM = "."
FRAME_EXTENSION = ".jpg"
VID_EXTENSION   = ".mp4"


def clean_components(dirname):
    names = listdir(dirname) # Should be just the audio by now mashallah
    for name in names:
        remove(path.join(dirname, name))
    rmdir(dirname)


def colour_pixel(colours):
    rgb = COLOUR_SEP.join([str(v) for v in colours])

    return ANSI_FN_CALL + SET_RGB + rgb + SGR + BLOCK


def download(link):
    title = None
    try:
        youtubeObject = YouTube(link)
    except:
        print(NOT_A_LINK)
    else:
        try:
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            title = youtubeObject.title + VID_EXTENSION
        except URLError:
            print(NO_INTERNET)
        except AgeRestrictedError:
            print(AGE_RESTRICTED)
        except VideoUnavailable:
            print(NOT_A_LINK)
        else:
            try:
                youtubeObject.download(filename = title)
            except:
                try:
                    remove(title)
                except:
                    pass
                title = None
                print(DOWNLOAD_FAIL)

    return title


def flipbook(art, framerate):
    frame_diff = 1 / framerate
    for i in art:
        start_time = datetime.now()
        system(WIPE_SCREEN)
        print(i)
        while ((datetime.now() - start_time).total_seconds() < frame_diff):
            pass


def imgs_to_ansi(dirname, frames, framerate, dims):
    ansis = []
    for frame in range(frames):
        nam = path.join(dirname, str(frame) + FRAME_EXTENSION)
        img = Image.open(nam)
        img = img.resize(dims)
        pix = img.load()
        ansis.append(pix_to_ascii(pix, dims))
        remove(nam)

    return ansis


def pix_to_ascii(pix, dims):
    width, height = dims
    art = ""
    for w in range(height):
        for h in range(width):
            art += colour_pixel(pix[h, w])
        art += linesep

    return art


def pull_frames(name):
    dirname = HIDDEN + sha256(name.encode(STR_ENCODING)).hexdigest()
    count   = 0
    frames  = 0
    try:
        mkdir(dirname)
    except FileExistsError:
        dirname = None
    else:
        vidcap = VideoCapture(name)
        success, image = vidcap.read()
        while success:
            imwrite(path.join(dirname, str(count) + FRAME_EXTENSION), image)
            success, image = vidcap.read()
            count += 1
        frames = vidcap.get(CAP_PROP_FPS)

    return dirname, count, frames


def rip_audio(dirname, video, frames):
    audio_path = path.join(dirname, AUDIO_FNAME)
    ffmpeg = FFmpeg().input(video).output(audio_path, AUDIO_OPS)
    ffmpeg.execute()

    return audio_path


def validate(argv):
    width, height = None, None
    if len(argv) == GOOD_ARGV:
        cands = argv[DIMS_IND].split(DIMS_DELIM)
        try:
            width, height = filter(lambda d : d > 0,    \
                    map(lambda x : int(x), cands))
        except ValueError:
            print(BAD_DIM_COUNT)
    else:
        print(BAD_ARGV)

    return width, height


def main():
    width, height = validate(argv)
    if width is None:
        exit(BAD_ARGS)

    print("Downloading video")
    title = download(argv[LINK_IND])
    if title is None:
        exit(BAD_VID)
    print("Download complete\nExtracting frames")

    dirname, frame_count, framerate = pull_frames(title)
    if dirname is None:
        # This will almost never happen organically
        print(ALREADY_EXISTS)
        exit(CANT_EXTRACT)

    print("Extracting audio")
    audio = rip_audio(dirname, title, framerate)
    remove(title)

    print("Extraction complete\nConverting images to ANSI")
    art = imgs_to_ansi(dirname, frame_count, framerate, (width, height))
    print("Conversion complete")
    sleep(2)

    audio_player = MediaPlayer(audio)
    audio_player.play()
    flipbook(art, framerate)
    audio_player.stop()
    clean_components(dirname)


if __name__ == "__main__":
    main()
