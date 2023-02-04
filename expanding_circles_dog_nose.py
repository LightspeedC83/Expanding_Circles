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


size = (1001, 1001) #setting the size for the image to be created
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

def coordinate_to_element(x,y): # will need to come back and adjust this to not graph a point that's not on the plane
    """Takes a coordinate on the coordiante plane (within the specified size for the image)
    and outputs the element in the list of pixels in the image that said coordinate pair corresponds to
    (ie. it takes ordered pair and converts it to a pixel on the image)"""

    if abs(x) <= horizontal_offset and abs(y) <= vertical_offset:
        return (x + horizontal_offset) + ((vertical_offset - y) *  size[1])
    else:
        return(None)

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

num_circles = 5
radius = 100
circles = []
for x in range(0, num_circles):
    start_zone_x = horizontal_offset - 2*radius
    start_zone_y = vertical_offset - 2*radius
    circles.append(Circle(h=random.randint(-start_zone_x, start_zone_x), k=random.randint(-start_zone_y, start_zone_y), radius=radius))

for frame in range(0,10):
    clear_pixel_list()
    radius += 10

    intersection_points = []

    for c in circles:
        c.radius = radius
        c.update_point_list()

        # checking whether or not the circles collide
        for other in circles:
            
            if not other is c:
                # for every circle, this part of the program loops over every other circle

                distance_between = math.sqrt((c.h - other.h)**2 + (c.k - other.k)**2)
                if (c.radius + other.radius) >= distance_between: #if the distance between the circles is less than or equal to the sum of their radii, then we know there must be some intersecting points --doesn't work quite yet
                    
                    # gets the angle between the point and the line between the circles' two centers, assuming that they are level (ie. same y value) and circle c is at the origin --using law of cosines
                    theta = math.acos(((other.radius**2)-(c.radius**2)-(distance_between**2))/(-2*c.radius*distance_between))
                     
                    # getting the amount the the line between the two centerpoints is rotated from the x-axis
                    phi = find_angle((other.k-c.k),(other.h-c.h))

                    # gets the points (x,y) where the circles intersect 
                    upper_intersection = (round(c.radius*math.cos(theta + phi)) + c.h ,round(c.radius*math.sin(theta + phi)) + c.k)
                    lower_intersection = (round(c.radius*math.cos(phi-theta)) + c.h ,round(c.radius*math.sin(phi-theta)) + c.k)

                    # print(upper_intersection, lower_intersection)
                    intersection_points.append(upper_intersection)
                    intersection_points.append(lower_intersection)


        c.graph_circle()


    output = Image.new(mode="RGB", size=size)

    output.putdata(pixel_list)

    output.save(f"{frame_output_folder}/{frame}-frame.jpg")


    # coloring in all the intersection points and marking each one with a small circle 
    for point in intersection_points:
        m = Circle(h=point[0], k=point[1], radius=5)
        m.update_point_list()
        m.graph_circle()

    output = Image.new(mode="RGB", size=size)

    output.putdata(pixel_list)

    output.save(f"{frame_output_folder}/{frame}-frame marked intersection.jpg")   

# saving all the frames as a video
frames = [frame_output_folder+"/"+f for f in os.listdir(frame_output_folder)] #getting a list of all the frame file paths

output_clip = me.ImageSequenceClip(frames, fps=1)
output_clip.write_videofile("ouput_animation.mp4", fps=1)  # is producing video that is a bit spotty, I think duplicate frames or frames that are out of order in output_frames is the culprit (it wasn't --still idk what is goin on)
