import unittest
from calcimetry.polyline import Polyline

class PolylineTest(unittest.TestCase):

    @staticmethod
    def create_polyline():
        return Polyline([
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


    def test_mean(self):
        polyline = PolylineTest.create_polyline()
        print(polyline.mean)

    def test_py(self):
        polyline = PolylineTest.create_polyline()

        print( polyline.p_y(3000))
        print( polyline.p_y(55))
        print( polyline.p_y(3210))


    def test_iter(self):
        polyline = PolylineTest.create_polyline()
        myiter = iter(polyline)
        for i, t in enumerate(myiter):
            x, y = t
            print(f"({i}) x:{x}, y:{y}")



if __name__ == '__main__':
    unittest.main()