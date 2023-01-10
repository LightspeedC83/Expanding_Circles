from PIL import Image
import math
import moviepy.editor as me
import os


frame_output_folder = "output_frames"
# clearing the frame_output_folder
for file in os.listdir(frame_output_folder):
    file = frame_output_folder + "/" + file
    os.remove(file)


size = (1001,1001) #setting the size for the image to be created
pixel_list = []

def clear_pixel_list():
    """populates the pixel_list list with all white pixel values according to the specified size of the image"""
    global pixel_list
    pixel_list = []
    for x in range(0,size[0]*size[1]): #generating all white values to populate the pixel list
        pixel_list.append((255,255,255))

clear_pixel_list() #creating an initial blank image

# getting horizontal and vertical offset from the center of the image to the top left 
# (used in converting coordinate to an element in the pixel list) 
horizontal_offset = size[0]//2 #for if (0,0) was at the top left
vertical_offset = size[1]//2

def coordinate_to_element(x,y):
    """Takes a coordinate on the coordiante plane (within the specified size for the image)
    and outputs the element in the list of pixels in the image that said coordinate pair corresponds to
    (ie. it takes ordered pair and converts it to a pixel on the image)"""

    return (x + horizontal_offset) + ((vertical_offset - y) *  size[1]) 



# drawing an expanding circle by going through each angle
radius = 0
for frame in range(0, 100):
    radius += 1
    for theta in range(0,3600):
        x = round(radius*math.cos(math.pi*theta/1800))
        y = round(radius*math.sin(math.pi*theta/1800))
        pixel_list[coordinate_to_element(x,y)] = (0,0,0)

    output = Image.new(mode="RGB", size=size)

    output.putdata(pixel_list)

    output.save(f"{frame_output_folder}/frame{frame}.jpg")
    clear_pixel_list()

# saving all the frames as a video
frames = [frame_output_folder+"/"+f for f in os.listdir(frame_output_folder)] #getting a list of all the frame file paths

output_clip = me.ImageSequenceClip(frames, fps=24)
output_clip.write_videofile("ouput_animation.mp4", fps=24)  # is producing video that is a bit spotty, I think duplicate frames or frames that are out of order in output_frames is the culprit
