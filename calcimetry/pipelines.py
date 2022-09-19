

def images_from_drills_pipeline(drills):
    pipeline = [
        { 
            "$match" : { 
                "DrillName" : { 
                    "$in" : drills
                }
            }
        }
    ]

    return pipeline