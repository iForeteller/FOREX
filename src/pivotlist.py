import pdb
from zigzag import *


class PivotList(object):
    '''
    Class that represents a list of Pivots as identified
    by the Zigzag indicator

    Class variables
    ---------------
    plist : list, Required
            List of pivots obtained using the 'peak_valley_pivots' function from Zigzag indicator
    slist : list, Derived
            Lisf of Segment objects connecting the pivot points. For obtaining these segments
            I use the function 'pivots_to_modes' implemented in the Zigzag indicator
    '''

    def __init__(self, plist):
        self.plist = plist

        # initializing the slist class member
        modes = pivots_to_modes(plist)

        segs = []
        count = 0
        type = None
        for i in modes:
            if type is None:
                type = i
                count += 1
                continue
            else:
                if i == type:
                    count += 1
                else:
                    s = Segment(type=type,
                                count=count)
                    type = i
                    count = 1
                    segs.append(s)

        segs.append(Segment(type=type, count=count))
        self.slist = segs

class Segment(object):
    '''
    Class containing a Segment object identified using the function 'get_segment_list' from the PivotList

    Class variables
    ---------------
    type : int, Required
           1 or -1
    count : int, Required
            Number of entities of 'type'
    '''

    def __init__(self, type, count):
        self.type = type
        self.count = count


'''
calc_angles()      
{
    angles = []

pdb.set_trace()
modes = pivots_to_modes(pivots)
y_vals = yarr[np.logical_or(pivots == 1, pivots == -1)]
x_vals = xarr[np.logical_or(pivots == 1, pivots == -1)]
slopes = []
x0 = None
y0 = None
for x, y in zip(x_vals, y_vals):
    if
x0 is None and y0 is None:
x0 = x
y0 = y
else:
slope = (y0 - y) / (x0 - x)
slopes.append(slope)
x0 = x
y0 = y

# calculate angle between segments (see documentation for formula)
m1 = None
for m2 in slopes:
    if
m1 is None: \
    m1 = m2
continue
tan_sigma = abs((m2 - m1) / (1 + m2 * m1))
angle = math.degrees(math.atan(tan_sigma))
angles.append(angle)
m1 = m2

}
'''