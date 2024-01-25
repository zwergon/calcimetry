
from calcimetry.mongo_api import MongoAPI, MongoInfo

big_query =  [
        { 
            "$lookup" : { 
                "from" : "vignettes", 
                "localField" : "MeasureId", 
                "foreignField" : "measurement", 
                "as" : "meas_vig"
            }
        }, 
        { 
            "$unwind" : { 
                "path" : "$meas_vig"
            }
        }, 
        { 
            "$project" : { 
               "meas_vig.ThuId" : 1.0, 
                "MeasureId" : 1.0, 
                "ImageId" : 1.0
            }
        },
        { 
            "$lookup" : { 
                "from" : "images", 
                "localField" : "ImageId", 
                "foreignField" : "ImageId", 
                "as" : "im_meas"
            }
        }, 
        { 
            "$unwind" : { 
                "path" : "$im_meas"
            }
        }, 
        { 
            "$addFields" : { 
                "DrillName" : "$im_meas.DrillName"
            }
        }, 
        { 
            "$group" : { 
                "_id" : "$DrillName", 
                "thumbnails" : { 
                    "$push" : "$meas_vig.ThuId"
                }
            }
        },
        { 
            "$out": {
             "db": "calcimetry",
             "coll": "thumbnails_by_drill"
            }
        }
        
    ] 

class NoteAPI(MongoAPI):

    IMG_COL = 'images'
    JPG_COL = 'jpgs'
    MES_COL = 'measurements'
    QUA_COL = 'quality'

    
    def __init__(self, mongo_info=MongoInfo()):
        super().__init__(mongo_info)

    def get_thumbnails_by_drill(self):
       

        results = {}
        docs = self.db["thumbnails_by_drill"].find({})
        for d in docs:
            results[d['_id']] = d['thumbnails']
        return results

    
if __name__ == "__main__":
    
    with NoteAPI() as note_api:
        thumbnails_by_drill = note_api.get_thumbnails_by_drill()
        print(thumbnails_by_drill)