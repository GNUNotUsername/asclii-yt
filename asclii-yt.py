from os                 import listdir, mkdir, path, remove, rmdir
from sys                import argv
from hashlib            import sha256
from cv2                import VideoCapture, imwrite, CAP_PROP_FPS
from pytube             import YouTube
from pytube.exceptions  import AgeRestrictedError, VideoUnavailable

# rm -rf .a9c222dfa89d082b3008456c3c722146b0e508083b703a044cdfe11a900f23fc ; python asclii-yt.py https://www.youtube.com/watch?v=QohH89Eu5iM 36x64

# Argv
DIMS_IND        = 2
GOOD_ARGV       = 3
LINK_IND        = 1

# Dimensions
DIMS_DELIM      = "x"

# Error messages
AGE_RESTRICTED  = "Age restricted videos cannot be downloaded"
ALREADY_EXISTS  = "Could not create a temporary directory to extract video frames"
BAD_ARGV        = "Usage: python3 asclii-yt.py link (width)x(height)"
BAD_DIM_COUNT   = "Two numeric frame dimensions are required"
BAD_LINK        = "Invalid youtube link provided"
DOWNLOAD_FAIL   = "Video could not be downloaded"
NOT_A_LINK      = "Link provided is not a youtube video"
F_NOT_SUPPORTED = "Only MP4 videos are supported presently"

# Exit values
BAD_ARGS        = 1
BAD_VID         = 2
NOT_SUPPORTED   = 3
CANT_EXTRACT    = 4

# Pathing
HIDDEN          = "."

# File Extensions
BEST_EXTENSION  = "mp4"
EXTENSION_DELIM = "."
FRAME_EXTENSION = ".jpg"


def clean_frames(dirname):
    names = listdir(dirname)
    for name in names:
        remove(path.join(dirname, name))
    rmdir(dirname)


def download(link):
    title = None
    try:
        youtubeObject = YouTube(link)
    except:
        print(NOT_A_LINK)
    else:
        try:
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            title = youtubeObject.title
        except AgeRestrictedError:
            print(AGE_RESTRICTED)
        except VideoUnavailable:
            print(NOT_A_LINK)
        else:
            try:
                youtubeObject.download()
            except:
                print(DOWNLOAD_FAIL)

    return title


def pull_frames(name):
    dirname = HIDDEN + sha256(name.encode("utf-8")).hexdigest()
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


def validate(argv):
    width, height = None, None
    if len(argv) == GOOD_ARGV:
        cands = argv[DIMS_IND].split(DIMS_DELIM)
        try:
            width, height = filter(lambda d : d > 0, map(lambda x : int(x), cands))
        except ValueError:
            print(BAD_DIM_COUNT)
    else:
        print(BAD_ARGV)

    return width, height


def main():
    width, height = validate(argv)
    if width is None:
        exit(BAD_ARGS)

    title   = download(argv[LINK_IND])
    if title is None:
        exit(BAD_VID)

    full    = list(filter(lambda p : p.startswith(title), listdir()))[0]
    extn    = full.split(EXTENSION_DELIM)[-1]
    if extn != BEST_EXTENSION:
        print(F_NOT_SUPPORTED)
        exit(NOT_SUPPORTED)

    dirname, frame_count, framerate = pull_frames(full)
    remove(full)
    if dirname is None:
        print(ALREADY_EXISTS)
        exit(CANT_EXTRACT)
    print(f"{frame_count} frames at {framerate} fps")

    clean_frames(dirname)


if __name__ == "__main__":
    main()
