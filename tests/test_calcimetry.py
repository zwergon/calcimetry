import unittest
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.mongo_api import MongoInfo

class CalcimetryTest(unittest.TestCase):

    HOST='localhost'
    PORT=27018

    def test_read_image(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            for i in range(1, 5):
                img = calcimetry_api.read_image(i)
                print(img)


    def test_get_drill_list(self):
        mongo_info = MongoInfo(host=CalcimetryTest.HOST, port=CalcimetryTest.PORT)
        with CalcimetryAPI(mongo_info=mongo_info) as calcimetry_api:
            print(calcimetry_api.get_drill_list())



if __name__ == '__main__':
    unittest.main()