import math, csv

#http://www.johndcook.com/python_longitude_latitude.html

'''
This script is basically a long way around to calculate the distances
between all of the bldgs and all of the amenities, this was used during
the hackathon because getting postgis up and running was taking too long
'''

'''
The following code returns the distance between to locations based 
on each point's longitude and latitude. The distance returned is 
relative to Earth's radius. To get the distance in miles, 
multiply by 3960. To get the distance in kilometers, multiply by 6373.
'''

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc


amenities = open('amenities_src.csv', 'r')
vacants = open('/home/dnfehren/projects/self/hviab/data/vacants_data.csv', 'r')

distances = open('/home/dnfehren/projects/self/hviab/data/amenities_data.csv', 'w')
d_writer = csv.writer(distances)

am_reader = csv.reader(amenities)
va_reader = csv.reader(vacants)

am = []
va = []

for va_row in va_reader:
    va.append([va_row[0], va_row[6], va_row[7]])

for am_row in am_reader:
    am.append(am_row)

for va_n, va_r in enumerate(va):

    #print va_r[2]

    if va_r[1] == 'Lat':
        continue

    for am_r in am:

        output = []

        if am_r[4] is not '':
            arc_dist = distance_on_unit_sphere(float(va_r[1]), 
                                                float(va_r[2]), 
                                                float(am_r[4]), 
                                                float(am_r[5]))
            dist = arc_dist * 3960

            output.append(va_r[0].replace(" ", "_").lower().replace(".",""))

            output.append(va_r[0])

            output.append(va_r[1])

            output.append(va_r[2])

            for am_r_e in am_r:
                output.append(am_r_e)

            output.append(dist)

            d_writer.writerow(output)

    print va_n
