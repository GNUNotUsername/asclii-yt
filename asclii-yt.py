from sys    import argv
from pytube import YouTube

# https://www.youtube.com/watch?v=yhB3BgJyGl8 for testing


# Argv
DIMS_IND        = 2
GOOD_ARGV       = 3

# Dimensions
DIMS_DELIM      = "x"

# Error messages
BAD_ARGV        = "Usage: python3 asclii-yt.py link (width)x(height)"
BAD_DIM_COUNT   = "Two numeric frame dimensions are required"
#BAD_DIM_VALS    = "Frame dimensions must be numeric"

# Exit values
BAD_ARGS        = 1

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

    print("Valid :)")

if __name__ == "__main__":
    main()
