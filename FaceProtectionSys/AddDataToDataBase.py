import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAcount.json")
firebase_admin.initialize_app(cred , {
    'databaseURL': ""
})

ref = db.reference('students')
data = {

    "20228":
        {
            "name" :"Amr Mamdouh",
            "major" : "Computer Science",
            "starting year" : 2021,
            "total attendance" : 3,
            "standing" : "G",
            "year" : 4 ,
            "last attendance" : "2024-10-1 00:54:23"
        },
        "20221":
        {
            "name" :"Elon Mask",
            "major" : "BIS",
            "starting year" : 2004,
            "total attendance" : 50,
            "standing" : "G",
            "year" : 4 ,
            "last attendance" : "2024-10-1 00:54:23"
        },
        "20225":
        {
            "name" :"Elina burk",
            "major" : "Computer Science",
            "starting year" : 2022,
            "total attendance" : 4,
            "standing" : "A",
            "year" : 1 ,
            "last attendance" : "2024-10-1 00:54:23"
        }
}

ref.update(data)
print("Done")
