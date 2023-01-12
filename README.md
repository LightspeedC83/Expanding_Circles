# Expanding Circles

I was looking at my dog's nose and the pattern of her skin intruiged me. This project attempts to recreate that pattern. 
The plan is to drop random points on a plane and have a circle expand from each point.
If two circles collide, the parts that are touching will not expand and the parts that aren't will continue to expand as usual.
I may also mess around with having them expand at random rates. 

# To Do:
- implement drawing circles via a class system --done
- find way of finding the resolution of a circle based on the radius --done (but not sure if done well)
- update graphing system so that it doesn't try to graph points on the plane
- graph multiple circles expanding from random points --done
- fix the animation glitching (it's not the order of the frames in the list)
- figure out circle collisions
    - lines 87-101 do detect if circles are colliding, it is just incredibly inefficient
- mess with rate of expansion