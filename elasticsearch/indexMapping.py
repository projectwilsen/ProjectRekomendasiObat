indexMapping = {
    "properties":{
        "id":{
            "type":"long"
        },
        "name":{
            "type":"text"
        },
        "uses":{
            "type":"text"
        },
        "uses_vector":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity": "l2_norm"
        }

    }
}