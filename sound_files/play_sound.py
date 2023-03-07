import winsound


def playsound(filename):
    winsound.PlaySound("filename", winsound.SND_FILENAME)