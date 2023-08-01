from PIL import Image
import math
import moviepy.editor as me
import os
import random


frame_output_folder = "output_frames"
# clearing the frame_output_folder
for file in os.listdir(frame_output_folder):
    file = frame_output_folder + "/" + file
    os.remove(file)


size = (5, 5) #setting the size for the image to be created
pixel_list = []

# function to clear the pixel list
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

#function that converts coordinants to list elements so they can be graphed
def coordinate_to_element(x,y): 
    """Takes a coordinate on the coordiante plane (within the specified size for the image)
    and outputs the element in the list of pixels in the image that said coordinate pair corresponds to
    (ie. it takes ordered pair and converts it to a pixel on the image)"""

    if abs(x) <= horizontal_offset and abs(y) <= vertical_offset:
        return (x + horizontal_offset) + ((vertical_offset - y) *  size[1])
    else:
        return(None)

# function that saves the pixel_list as an image
frame_count = 0
def save_image(file_directory):
    """Saves an image formed from the pixel_list and saves it to a given directory"""
    output = Image.new(mode="RGB", size=size)

    output.putdata(pixel_list)

    output.save(file_directory)
    global frame_count #system to keep track of the total nubmer of frames
    frame_count +=1
        
# function that finds an angle given opposite and adjacent side lengths
def find_angle(y,x): 
    """This function will return an angle given the x and y distances
    (ie. the two components of the vector or the opposite and adjacent sides of a right triangle). 
    It is important to note that the function uses arctan so its input is in (y,x) not (x,y) form"""

    if x > 0: #for if the angle is on the right half of the unit circle
        return(math.atan(y/x))
    elif x < 0: #for if the angle is on the left half of the unit circle
        return(math.atan(y/x) + math.pi)
    elif y > 0:
        return(math.pi/2)
    else:
        return(-math.pi/2)

# function that finds circle intersections
def find_intersection(c1,c2):
    """finds the points where two circles, c1 and c2, intersect.
    c1 and c2 are tuples in the form (h,k,r) or (x-offest, y-offset, radius)"""

    h1 = c1[0] # x value of first circle's origin
    k1 = c1[1] # y value of first circle's origin
    r1 = c1[2] # radius of first circle

    h2 = c2[0] # x value of second circle's origin
    k2 = c2[1] # y value of second circle's origin
    r2 = c2[2] # radius of second circle

    distance = math.sqrt((h2-h1)**2 + (k2-k1)**2)

    if distance > r1+r2: # if the distance between the two circles is bigger than both radii, then there are not intersections
        return None
    elif distance < abs(r1-r2): # if one circle is contained inside the other, there won't be an intersection
        return None
    else: # if the circles intersect
        theta = math.acos(((r2**2 - r1**2 - distance**2)/(-2*r1*distance))) # the angle between the line connecting the circle's centers and the line from c1 to the intersection point

        phi = find_angle((k2-k1),(h2-h1)) # the angle offset from the positive x axis to the distance between the two circles

        point_1 = ((r1*math.cos(phi+theta)) + h1), ((r1*math.sin(phi+theta)) + k1)
        point_2 = ((r1*math.cos(phi-theta)) + h1), ((r1*math.sin(phi-theta)) + k1)

        return (point_1, point_2)

# creating a circle class
class Circle:
    """is a circle with center at point (h,k) and a radius of radius."""
    def __init__(self, h, k, radius):
        self.h = round(h)
        self.k = round(k)
        self.radius = radius
        self.point_list = []
        
        # finding resolution of circle
        if radius < 50:
            self.resolution = 10
        else:
            self.resolution = radius//3 # todo: there is probably a smart way of figuring out what the resolution needs to be based on the radius

    def update_point_list(self):
        self.point_list = []
        # getting a list of points that fall on the circle
        for theta in range(0,(360*self.resolution)):  #isn't updating circle position b/c it only runs this code on initialization
            x = self.h + round(self.radius*math.cos(math.pi*theta/(180*self.resolution)))
            y = self.k + round(self.radius*math.sin(math.pi*theta/(180*self.resolution)))
            self.point_list.append((x,y))
        
    def graph_circle(self):
        """graphs the circle with the parameters given at its creation""" 
        for point in self.point_list:
            point_element = coordinate_to_element(point[0], point[1])
            if not point_element == None:
                pixel_list[point_element] = (0,0,0) #graphs the point on the plane

# # creating a list of circle objects
# num_circles = 5
# radius = 100
# circles = []
# for x in range(0, num_circles):
#     # making sure the circles are created a certain distance away from the edge
#     start_zone_x = horizontal_offset - 2*radius
#     start_zone_y = vertical_offset - 2*radius
#     circles.append(Circle(h=random.randint(-start_zone_x, start_zone_x), k=random.randint(-start_zone_y, start_zone_y), radius=radius))

# # starting the simulation of expanding the circles
# for frame in range(0,10):
    # clear_pixel_list()
    # radius += 10

    # intersection_points = []

    # temp_list_of_circles = circles[:]
    # for c in temp_list_of_circles:
    #     c.radius = radius
    #     c.update_point_list()

    #     # checking whether or not the circles collide
    #     for other in temp_list_of_circles:
            
    #         if not other is c:
    #             # for every circle, this part of the program loops over every other circle

    #                 # gets the points (x,y) where the circles intersect and rounding them to nearest integer
    #                 intersections =  find_intersection((c.h, c.k, c.radius), (other.h, other.k, other.radius))
    #                 if intersections == None:
    #                     continue
    #                 upper_intersection, lower_intersection = intersections
    #                 upper_intersection, lower_intersection = (round(upper_intersection[0]), round(upper_intersection[1])), (round(lower_intersection[0]), round(lower_intersection[1]))

    #                 # print(upper_intersection, lower_intersection)
    #                 intersection_points.append(upper_intersection)
    #                 intersection_points.append(lower_intersection)


    #     c.graph_circle()
    #     # if the below line of code is uncommented, it should only consider circles once (which is good), but this messes eveerything up for some reason (which is bad)
    #     # temp_list_of_circles.remove(c) # removing the circle we just checked from consideration during this "frame"




    # output = Image.new(mode="RGB", size=size)

    # output.putdata(pixel_list)

    # output.save(f"{frame_output_folder}/{frame}-frame.jpg")


    # # marking each intersection point with a small circle 
    # for point in intersection_points:
    #     m = Circle(h=point[0], k=point[1], radius=5)
    #     m.update_point_list()
    #     m.graph_circle()

    # output = Image.new(mode="RGB", size=size)

    # output.putdata(pixel_list)

    # output.save(f"{frame_output_folder}/{frame}-frame marked intersection.jpg")   

#checking the varacity of the coordinate to element function -- all seems to be good
count = 0
for x in range(-1*horizontal_offset, horizontal_offset):
    for y in range(-1*vertical_offset+1, vertical_offset+1):
        element = coordinate_to_element(x,y)
        if element != None:
            pixel_list[element] = (0,0,0)
            save_image(f"{frame_output_folder}/{count}.jpg")
        else:
            print(x,y)

        count += 1

# function that saves all the frames as a video
def make_video():
    frames = [frame_output_folder+"/"+str(f)+".jpg" for f in range(frame_count)] #getting a list of all the frame file paths

    output_clip = me.ImageSequenceClip(frames, fps=30)
    output_clip.write_videofile("ouput_animation.mp4", fps=30)  # is producing video that is a bit spotty, I think duplicate frames or frames that are out of order in output_frames is the culprit (it wasn't --still idk what is goin on)

make_video() #calling that function