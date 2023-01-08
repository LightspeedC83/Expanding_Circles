from PIL import Image
import math

#deciding what cooridinates need to be drawn

size = (1001,1001) #setting the size for the image to be created
pixel_list = []

for x in range(0,size[0]*size[1]): #generating all white values to populate the pixel list
    pixel_list.append((255,255,255))

#first finding the center pixel of the grid 
horizontal_offset = size[0]//2 #for if (0,0) was at the top left
vertical_offset = size[1]//2

def coordinate_to_element(x,y):
    """Takes a coordinate on the coordiante plane (within the specified size for the image)
    and outputs the element in the list of pixels in the image that said coordinate pair corresponds to
    (ie. it takes ordered pair and converts it to a pixel on the image)"""

    return (x + horizontal_offset) + (((vertical_offset - y)) *  size[1]) #something is fucking up when y<0

#testing out coordinate system with simple line
# for x in range(-100,101):
#     pixel_list[coordinate_to_element(x,x)] = (0,0,0)

# This tries to make a circle half --does not work (seems to be some sort of sqrt funciton)
# radius = 100
# for x in range(-100,101):
#     radicand = (radius^2) - (x^2)
#     if radicand >=0:
#         y = math.sqrt(radicand)
#         y_closest = round(y)
        
#         pixel_list[coordinate_to_element(x,y_closest)] = (0,0,0)
#         pixel_list[coordinate_to_element(x,-1*y_closest)] = (0,0,0) # (this sideways parabola definitely shows that it's doing a sqrt function and not circle as intended)

#drawing those coordinates and saving the frame
output = Image.new(mode="RGB", size=size)

output.putdata(pixel_list)

output.show()
