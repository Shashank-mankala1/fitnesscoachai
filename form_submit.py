from db import personal_profiles_collection, notes_collection
from datetime import datetime

def update_profile(existing, update_type,**kwargs):
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
        update_field = {"goals": existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}

    personal_profiles_collection.update_one(
        {"_id": existing["_id"]}, {"$set": update_field}
    )
    return existing


def add_note(profile_id, note):
    new_entry = {
        "user_id": profile_id,
        "text": note,
        "$vectorize": note,
        "metadata": {"injested":datetime.now()},
    }
    res=notes_collection.update_one(new_entry)
    new_entry["_id"] = res.inserted_id
    return new_entry

def delete_note(note_id):
    notes_collection.delete_one({"_id": note_id})