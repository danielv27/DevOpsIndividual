import os
import tempfile
from functools import reduce
import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongo")
db = client.db
students = db.students


def add(student=None):
    if students.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return 'user already exists', 409

    result = students.insert_one(student.to_dict())
    return str(result.inserted_id)

def get_by_id(student_id=None, subject=None):
    student = students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'user not found', 404
    
    student['student_id'] = str(student['_id'])
    del student['_id']
    return student

def delete(student_id=None):
    student = students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404
    res = students.delete_one({"_id": ObjectId(student_id)})
    return str(student['_id'])