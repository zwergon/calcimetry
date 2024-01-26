
from calcimetry.mongo_api import MongoAPI, MongoInfo

def get_pipeline(collection):
    return [
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
                "quality" : 1.0, 
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
                    "$push" : { 
                        "ThuID" : "$meas_vig.ThuId", 
                        "quality" : "$quality"
                    }
                }
            }
        }, 
        { 
            "$out" : { 
                "db" : "calcimetry", 
                "coll" : collection
            }
        }
    ]
        
class NoteAPI(MongoAPI):

    IMG_COL = 'images'
    JPG_COL = 'jpgs'
    MES_COL = 'measurements'
    QUA_COL = 'quality'
    THU_COL = 'thumbnails_by_drill'

    
    def __init__(self, mongo_info=MongoInfo()):
        super().__init__(mongo_info)

    def update_thumbnails(self):
        print("update_thumbnails")
        self.db.drop_collection(NoteAPI.THU_COL)
        self.db[NoteAPI.MES_COL].aggregate(get_pipeline(NoteAPI.THU_COL))

    def get_thumbnails_by_drill(self, all:bool = False):
        results = {}
        docs = self.db[NoteAPI.THU_COL].find({})
        for d in docs:
            thumbnails = d['thumbnails']
            todo = []
            for t in thumbnails:
                if all or t['quality'] == 10:
                   todo.append(t['ThuID'])
            if len(todo) > 0:
                results[d['_id']] = todo
        return results
    
    def update_note(self, measure_id, note):
        self.db[self.MES_COL].update_one(
            filter={"MeasureId": measure_id},
            update={
                "$set": {
                    "quality": note,
                }
            }
        )


    
if __name__ == "__main__":
    
    with NoteAPI() as note_api:
        thumbnails_by_drill = note_api.get_thumbnails_by_drill()
        print(thumbnails_by_drill)