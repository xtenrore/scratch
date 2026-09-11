# Clean metadata copy helper removing "raw"
def clean_costume(c):
    return {
        "name": c["name"],
        "assetId": c["assetId"],
        "dataFormat": c["dataFormat"],
        "md5ext": c["md5ext"],
        "rotationCenterX": c["rotationCenterX"],
        "rotationCenterY": c["rotationCenterY"]
    }

def clean_sound(s):
    return {
        "name": s["name"],
        "assetId": s["assetId"],
        "dataFormat": s["dataFormat"],
        "format": s["format"],
        "rate": s["rate"],
        "sampleCount": s["sampleCount"],
        "md5ext": s["md5ext"]
    }
