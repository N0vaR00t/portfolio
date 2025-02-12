"""
Name: Diana Nykonenko
ID: 001265364
Date: 08/03/2023
"""

"""
We assume that:
1) The planet surface is flat and infinite 
2) All the planes fly on the same high and speed.
Question: 
We have lines that represent ways of each plane. 
For every line we have two points on the coordinate system that we can see as the plane radar.
We can have unlimited number of lines depending on what user will enter. 
The program needs to find points where lines intersect and print the points of intersection for all the lines. 
Lines are infinite.
"""

"""
a1x + b1y + c1 = 0 
a2x + b2y + c2 = 0
(x,y) = (b1c2 - b2c1 / a1b2 - a2b1, a2c1 - a1c2 / a1b2 - a2b1)
"""

import time

# creating lines list
lines = []
while True:
    new_line = input("Please enter the coordinates of the line as four numbers. Enter 'go' to proceed: ")
    # breaking the loop
    if new_line == "go":
        break
    try:
        coordinates = list(map(float, new_line.split()))
        # only accepting four float/int numbers in a row  like 1 2 3 4
        if len(coordinates) != 4:
            raise ValueError
        point1 = (coordinates[0], coordinates[1])
        point2 = (coordinates[2], coordinates[3])
        lines.append((point1, point2))
    except ValueError:
        print("Invalid input, please enter the coordinates as four integers separated by spaces. 'go' to proceed:")

print(lines)

start_time = time.time()
# starting time recording


def intersection(lines):
    lines = sorted(lines, key=lambda line: min(line[0][0], line[1][0]))
    intersections = []
    active_lines = []

    for line in lines:

        active_lines.append(line)

        for other_line in active_lines:
            if other_line == line:
                continue
            # formulas
            # x = (b1*c2 - b2*c1) / (a1*b2 - a2*b1)
            # y = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)

            a1, b1, c1 = line[1][1] - line[0][1], line[0][0] - line[1][0], line[0][0] * line[1][1] - line[1][0] * \
                         line[0][1]
            a2, b2, c2 = other_line[1][1] - other_line[0][1], other_line[0][0] - other_line[1][0], other_line[0][0] * \
                         other_line[1][1] - other_line[1][0] * other_line[0][1]

            denom = a1 * b2 - a2 * b1
            if denom == 0:
                # lines are parallel
                continue

            x_intersect = (b2 * c1 - b1 * c2) / denom
            y_intersect = (a1 * c2 - a2 * c1) / denom
            intersections.append((x_intersect, y_intersect))
    return intersections

end_time = time.time()
# end of time recording
total_time = end_time - start_time
print("Total time taken by calculations: {:.10f} seconds".format(total_time))

if not intersection(lines):
    # if no intersections were found
    print("All routes are safe")
else:
    print("Potentially dangerous coordinates are:", intersection(lines))
    # prints all intersection coordinates
