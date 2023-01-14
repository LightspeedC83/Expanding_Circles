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

    return (x + horizontal_offset) + ((vertical_offset - y) *  size[1]) 

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
            try:
                pixel_list[coordinate_to_element(point[0], point[1])] = (0,0,0) #graphs the point on the plane
                
            except IndexError:
                print("tried to graph a point not on the plane")
                # raise IndexError("tried to graph a point not on the plane") # may not have 

num_circles = 5
radius = 50
circles = []
for x in range(0, num_circles):
    circles.append(Circle(h=random.randint(-250,250), k=random.randint(-250,250), radius=radius))

for frame in range(0,1):
    clear_pixel_list()
    radius += 1

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
                    theta = math.acos(((other.radius**2)-(c.radius**2)-(distance_between**2))/(2*c.radius*distance_between))

                    # gets the points (x,y) where the circles intersect 
                    upper_intersection = (c.radius*math.cos(theta),c.radius*math.sin(theta))
                    lower_intersection = (upper_intersection[0], -1*upper_intersection[1])

                    # getting the amount the the line between the two centerpoints is rotated from the x-axis
                    phi = math.atan((other.k-c.k)/(other.h-c.h))

                    # rotating our two intersection points by phi and translating them by the circle center offset yielding our upper and lower intersection points
                    y_upper = round(upper_intersection[1]*math.cos(phi) + upper_intersection[0]*math.sin(phi) + c.k)
                    x_upper = round(upper_intersection[0]*math.cos(phi) - upper_intersection[1]*math.sin(phi) + c.h)

                    x_lower = round(lower_intersection[0]*math.cos(phi) - lower_intersection[1]*math.sin(phi) + c.h)
                    y_lower = round(lower_intersection[1]*math.cos(phi) + lower_intersection[0]*math.sin(phi) + c.k)

                    # adding the intersection points to our list of intersection points for this frame
                    intersection_points.append((x_upper, y_upper))
                    intersection_points.append((x_lower, y_lower))

        c.graph_circle()


    #coloring in all the intersection points
    for point in intersection_points:
        pixel_list[coordinate_to_element(point[0],point[1])] = (0,0,255)

    output = Image.new(mode="RGB", size=size)

    output.putdata(pixel_list)

    output.save(f"{frame_output_folder}/{frame}-frame.jpg")

# saving all the frames as a video
frames = [frame_output_folder+"/"+f for f in os.listdir(frame_output_folder)] #getting a list of all the frame file paths

output_clip = me.ImageSequenceClip(frames, fps=24)
output_clip.write_videofile("ouput_animation.mp4", fps=24)  # is producing video that is a bit spotty, I think duplicate frames or frames that are out of order in output_frames is the culprit (it wasn't --still idk what is goin on)
