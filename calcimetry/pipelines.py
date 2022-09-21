

from cmath import nan


def image_selection_pipeline(drills, #cotes_min_max,
                             cotemin, cotemax, resomin, resomax, yratmin, yratmax, nmesmin, nmesmax):
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
    # if cotes_min_max is not None:
    #     pipeline[0]['$match']['$and'].append( {"Cote0": {"$gte": cotes_min_max[0]}} )
    #     pipeline[0]['$match']['$and'].append( {"Cote1": {"$lte": cotes_min_max[1]}} )

    for (condmin, prop) in [(cotemin, "Cote0"), (resomin, "criteria.resolution"), (yratmin, "criteria.y_ratio"),
                            (nmesmin, "criteria.n_measurements")]:
        if condmin is not None:
            pipeline[0]['$match']['$and'].append( {prop: {"$gte": condmin}} )

    for (condmax, prop) in [(cotemax, "Cote0"), (resomax, "criteria.resolution"), (yratmax, "criteria.y_ratio"),
                            (nmesmax, "criteria.n_measurements")]:
        if condmax is not None:
            pipeline[0]['$match']['$and'].append( {prop: {"$lte": condmax}} )

    #print(pipeline)

    return pipeline

def min_max_criteria():
    pipeline =     [
        { 
            "$match" : { 
                "px0" : { 
                    "$ne" : nan
                }, 
                "criteria.y_ratio" : { 
                    "$gt" : 0.0
                }
            }
        }, 
        { 
            "$group" : { 
                "_id" : None, 
                "min_nb" : { 
                    "$min" : "$criteria.n_measurements"
                }, 
                "max_nb" : { 
                    "$max" : "$criteria.n_measurements"
                }, 
                "min_res" : { 
                    "$min" : "$criteria.resolution"
                }, 
                "max_res" : { 
                    "$max" : "$criteria.resolution"
                }, 
                "avg_res" : { 
                    "$avg" : "$criteria.resolution"
                }, 
                "min_y_ratio" : { 
                    "$min" : "$criteria.y_ratio"
                }, 
                "max_y_ratio" : { 
                    "$max" : "$criteria.y_ratio"
                }, 
                "avg_y_ratio" : { 
                    "$avg" : "$criteria.y_ratio"
                }
            }
        }
    ]
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
