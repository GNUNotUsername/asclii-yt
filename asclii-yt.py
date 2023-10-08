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

# Exit values
BAD_ARGS        = 1


def download(link):
    try:
        youtubeObject = YouTube(link)
    except:
        print(NOT_A_LINK)
    else:
        try:
            youtubeObject = youtubeObject.streams.get_highest_resolution()
        except AgeRestrictedError:
            print(AGE_RESTRICTED)
        except VideoUnavailable:
            print(NOT_A_LINK)
        else:
            try:
                youtubeObject.download()
            except:
                print(DOWNLOAD_FAIL)


def validate(argv):
    width, height = None, None
    if len(argv) == GOOD_ARGV:
        cands = argv[DIMS_IND].split(DIMS_DELIM)
        try:
            width, height = filter(lambda x : x > 0, map(lambda x : int(x), cands))
        except ValueError:
            print(BAD_DIM_COUNT)
    else:
        print(BAD_ARGV)

    return width, height

def main():
    width, height = validate(argv)
    if width is None:
        exit(BAD_ARGS)

    download(argv[LINK_IND])

    print("Valid :)")

if __name__ == "__main__":
    main()
