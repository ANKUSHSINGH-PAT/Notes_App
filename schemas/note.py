def noteentity(item)->dict:
    return {
        "id": str(item["_id"]),
        "title": str(item["title"]),
        "desc": item["desc"],
        "important": item["important"],

    }

def notesentity(items)->dict:
    return [noteentity(item) for item in items]