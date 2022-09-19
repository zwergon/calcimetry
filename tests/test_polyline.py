import unittest
from calcimetry.polyline import Polyline

class PolylineTest(unittest.TestCase):


    def test_mean(self):
        polyline = Polyline([
            [55, 173], 
            [259, 179], 
            [430, 177], 
            [583, 171], 
            [723, 184], 
            [1113, 178], 
            [1432, 187], 
            [1562, 190], 
            [1634, 193], 
            [1930, 194], 
            [2599, 202], 
            [3210, 211]]
            )
        print(polyline.mean)

        print( polyline.p_y(3000))
        print( polyline.p_y(55))
        print( polyline.p_y(3210))
        



if __name__ == '__main__':
    unittest.main()