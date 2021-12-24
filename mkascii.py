import sys,os
import imp
import PIL.Image
import subprocess
from os import get_terminal_size as _term_size

def convert_frame_pixels_to_ascii(frame,dimensions, new_line_chars=True):
    """
    Replace all pixeles with colored chars and return the resulting string

    This method iterates each pixel of one video frame
    respecting the dimensions of the printing area
    to truncate the width if necessary
    and use the pixel_to_ascii method to convert one pixel
    into a character with the appropriate color.
    Finally joins the set of chars in a string ready to print.

    Args:
        frame: a single video frame
        dimensions: an array with the printing area dimensions
            in pixels [rows, cols]
        new_line_chars: if should append a new line character
            at end of each row

    Returns:
        str: The resulting set of colored chars as a unique string

    """
    cols, _ = dimensions
    w, h = frame.size

    printing_width = int(min(int(cols), (w*2))/2)
    pad = max(int(cols) - printing_width*2, 0) 
        
    
    msg = ''
    for i in range(h-2):
        for j in range(printing_width-2):
            pixel = frame.getpixel((j,i))
            msg += imp.pixel_to_ascii(pixel)
        if new_line_chars:
            msg += "\n"
        else:
            msg += " " * (pad)
    msg += "\r\n"
    return msg

def resize(frame, dimensions):
    width, height = frame.size
    _, rows = dimensions
    reduction_factor = (float(rows)) / height * 100
    reduced_width = int(width * reduction_factor / 100)
    reduced_height = int(height * reduction_factor / 100)
    dimension = (reduced_width, reduced_height)
    print(f'resizing {dimension}')
    return frame.resize(dimension)
def show(name):
    try:
        for i in range(1,1000):
            resolution = _term_size()
            fname = "data/images/{file}/output{f:0=6}.png".format(f = i,file=name)
            with PIL.Image.open(fname) as frame:
                frame = resize(frame,resolution)
                sys.stdout.write(convert_frame_pixels_to_ascii(frame,resolution))
    except KeyboardInterrupt:
        print('exiting')

def gen(input):
    output = input.split('/')[-1].split('.')[0]
    if not os.path.exists("data/images/" + output):
        os.makedirs("data/images/" + output)

    query = "ffmpeg -i " + input + " -vf fps=" + str(15) + " " + "data/images/" + output + "/output%06d.png"
    response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()

def main():
    os.system("clear")
    dd = "data/images/"
    all = os.listdir(dd)
    lst = {}
    for a in range(len(all)):
        if os.path.exists(f'{dd}{all[a]}/output000001.png'):
            lst[str(a)] = all[a]
    print(lst)
    chose = input("chose number of video: ")
    if chose in lst:
        show(lst[chose])
    elif chose == "":
        path = input("Paste path to mp4 here: ")
        if os.path.exists(path):
            gen(path)
        else:
            print("invalid path")
    else:
        print("Invalid input")
#gen("/home/wex/Downloads/cipa.mp4")
if __name__ == "__main__":
    while True:
        main()




