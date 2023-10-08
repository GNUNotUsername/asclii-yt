from os                 import listdir
from sys                import argv
from pytube             import YouTube
from pytube.exceptions  import AgeRestrictedError, VideoUnavailable

# https://www.youtube.com/watch?v=yhB3BgJyGl8 for testing


# Argv
DIMS_IND        = 2
GOOD_ARGV       = 3
LINK_IND        = 1

# Dimensions
DIMS_DELIM      = "x"

# Error messages
AGE_RESTRICTED  = "Age restricted videos cannot be downloaded"
BAD_ARGV        = "Usage: python3 asclii-yt.py link (width)x(height)"
BAD_DIM_COUNT   = "Two numeric frame dimensions are required"
BAD_LINK        = "Invalid youtube link provided"
DOWNLOAD_FAIL   = "Video could not be downloaded"
NOT_A_LINK      = "Link provided is not a youtube video"
F_NOT_SUPPORTED = "Only MP4 videos are supported presently"

# Exit values
BAD_ARGS        = 1
NOT_SUPPORTED   = 2

# Video files
BEST_EXTENSION  = "mp4"
EXTENSION_DELIM = "."



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


def get_vids():
    return set(filter(lambda p : p.endswith(".mp4"), listdir()))


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
    full    = list(filter(lambda p : p.startswith(title), listdir()))[0]
    extn    = full.split(EXTENSION_DELIM)[-1]
    if extn != BEST_EXTENSION:
        print(F_NOT_SUPPORTED)
        exit(NOT_SUPPORTED)

    print("Supported :)")


if __name__ == "__main__":
    main()
