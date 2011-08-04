from google.appengine.ext import db

class departmentdb(db.Model):
    department = db.StringProperty(required = True)
    add_time = db.DateTimeProperty(auto_now = True)
    added_by = db.UserProperty(required = True)

class subjectdb(db.Model):
    subject = db.StringProperty(required = True)
    department = db.ReferenceProperty(departmentdb)
    add_time = db.DateTimeProperty(auto_now = True)
    added_by = db.UserProperty(required = True)

class questiondb(db.Model):
    subject = db.ReferenceProperty(subjectdb)
    question_type =db.StringProperty(required=True, choices=set(["PartA", "PartB"]))
    question = db.TextProperty(required = True)
    add_time = db.DateTimeProperty(auto_now = True)
    added_by = db.UserProperty(required = True)

