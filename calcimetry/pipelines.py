

def image_selection_pipeline(drills, cotes_min_max):
    pipeline = [
        {
            "$match": {
                "$and": []
            }
        },
        {
            "$project": {
                "_id": 0,
                "ImageId": 1
            }
        }
    ]

    if drills is not None:
        pipeline[0]['$match']['$and'].append( {"DrillName": {"$in": drills}} )

    # add some "cote" constraints in match stage of the pipeline
    if cotes_min_max is not None:
        pipeline[0]['$match']['$and'].append( {"Cote0": {"$gte": cotes_min_max[0]}} )
        pipeline[0]['$match']['$and'].append( {"Cote1": {"$lte": cotes_min_max[1]}} )

    #print(pipeline)

    return pipeline


def extra_params_pipeline():
    pipeline = [
        # {
        #     "$addFields": {
        #         "resolution": {
        #             "$function": {
        #                 "body": function(p0, p1, c0, c1){
        #                     return Math.abs((c0-c1)/(p0-p1))
        #                 },
        #                 "args": [
        #                     "$px0",
        #                     "$px1",
        #                     "$Cote0",
        #                     "$Cote1"
        #                 ],
        #                 "lang": "js"
        #             }
        #         },
        #         "k_up_mean": {
        #             "$avg": {
        #                 "$map": {
        #                     "input": "$k_Up",
        #                     "as": "xy_up",
        #                     "in": {
        #                         "$last": "$$xy_up"
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }
    ]

    return pipeline
