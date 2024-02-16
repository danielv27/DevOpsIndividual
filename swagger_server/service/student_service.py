import os
import tempfile
from functools import reduce
import json
from pymongo import MongoClient
from bson import ObjectId

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.db
students = db.students
counts = db.counts


def add(student=None):
    if students.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return 'user already exists', 409

    count = 0
    count_object = counts.find_one({"name": "student_count"})
    if not count_object:
        counts.insert_one({"name": "student_count", "value": 0})
        count = 1
    else:
        count = count_object.get("value") + 1
        counts.update_one({"name": "student_count"}, {"$set": {"value": count}})

    student.student_id = count

    students.insert_one(student.to_dict())
    return count, 200

def get_by_id(student_id=None, subject=None):
    student = students.find_one({"student_id": student_id})
    if not student:
        return 'user not found', 404
    
    del student['_id']
    return student, 200

def delete(student_id=None):
    student = students.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404
    students.delete_one({"student_id": student_id})
    return student_id, 200