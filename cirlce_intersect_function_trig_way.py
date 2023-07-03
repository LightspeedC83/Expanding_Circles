import math

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

c1 = (4,5,5)
c2 = (2,5,5)

print(find_intersection(c1,c2))