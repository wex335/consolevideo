import sys,os
import imp
import PIL.Image
import subprocess
from os import get_terminal_size as _term_size


def convert_frame_pixels_to_ascii(frame,dimensions, new_line_chars=True):
    cols, _ = dimensions
    w, h = frame.size

    printing_width = int(min(int(cols), (w*2))/2)
    pad = max(int(cols) - printing_width*2, 0) 
        
    
    msg = ''
    for i in range(h-2):
        for j in range(printing_width-2):
            pixel = frame.getpixel((j,i))
            msg += imp.pixel_to_ascii(pixel,density=3)
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
    return frame.resize(dimension)
def show(name):
    try:
        files = os.listdir(f"{name}/")
        for i in range(1,len(files)):
            resolution = _term_size()
            fname = "{file}/output{f:0=6}.png".format(f = i,file=name)
            with PIL.Image.open(fname) as frame:
                sys.stdout.write('\u001b[0;0H')
                frame = resize(frame,resolution)
                sys.stdout.write(convert_frame_pixels_to_ascii(frame,resolution))
    except KeyboardInterrupt:
        print('exiting')

def frame(frame):
    resolution = _term_size()
    sys.stdout.write('\u001b[0;0H')
    sys.stdout.write(str(resolution))
    frame = resize(frame,resolution)
    sys.stdout.write(convert_frame_pixels_to_ascii(frame,resolution))
def gen(input):
    output = input.split('/')[-1].split('.')[0]
    if not os.path.exists("./" + output):
        os.makedirs("./" + output)

    query = "ffmpeg -i " + input + " -vf fps=" + str(15) + " ." + "/" + output + "/output%06d.png"
    os.system(query)

def main():
    os.system("clear")
    dd = "./"
    all = os.listdir(dd)
    lstd = {}
    lstv = {}
    for a in range(len(all)):
        if os.path.exists(f'{dd}{all[a]}/output000001.png'):
            lstd[str(a)] = all[a]
        elif all[a].endswith('.mp4'):
            lstv[str(a)] = all[a]
    
    print(lstd)
    chose = input("chose number of video: ")
    if chose in lstd:
        show(lstd[chose])
    elif chose == "":
        print(lstv)
        path = input("Paste path to mp4 here: ")
        if path in lstv:
            gen(lstv[path])
        elif os.path.exists(path):
            gen(path)
        else:
            print("invalid path")
    else:
        print("Invalid input")
#gen("/home/wex/Downloads/cipa.mp4")
if __name__ == "__main__":
    while True:
        main()




