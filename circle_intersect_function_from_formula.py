"""this way should work excepting when the circles are have the same y offsets, but it doesn't seem to --idk why"""

import math

def find_intersection(c1, c2):
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
        """This is done by setting the equations of both circles equal to eachother and simplifying to get the equation for the line that passes through both intersection points (in the form y=mx+b).
        y can then be substituted into one of the circle equations and this simplifies into a quadratic equation. The quadratic formula is used to find the x values of the intersection points.
        These x values are plugged into the line equation (y=mx+b) to get their corresponding y values, giving the intersection points."""
        # finding the line (in the form y=mx+b) that intersects the intersection points
        m = (h2-h1) / (k1-k2)
        b = ((h1**2 + k1**2 + r2**2)-(h2**2 + k2**2 + r1**2)) / (2*(k1 - k2))

        # getting the a,b,c values to use in quadratic fomula
        A = m**2 -1
        B = 2*((m*(b-k1))-h1)
        C = h1**2 + (b-k1)**2 - r1**2

        # using quadratic forumula to find the x values
        if B**2 - 4*A*C < 0: # if the solution is complex it returns none b/c the circles won't intersect on the cartesian plane (the two checks above should stop this from happening though)
            return None
        else:
            x1 = (-B + math.sqrt(B**2 - 4*A*C)) / (2*A)
            x2 = (-B - math.sqrt(B**2 - 4*A*C)) / (2*A) 

            point_1, point_2 = (x1, (m*x1+b)), (x2, (m*x2+b))

            return [point_1, point_2]

c1 = (4,5,5)
c2 = (0,10,5)

print(find_intersection(c1,c2))