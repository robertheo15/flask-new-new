from datetime import datetime, timedelta, date
import uuid
import pymongo
today = date.today()
# yesterday = today - timedelta(days = 1)
yesterday = date.today() - timedelta(1)
# yesterday = datetime.now() - timedelta(1)
now = datetime.now()
# now = now.replace(hour=8, minute=0, second=0, microsecond=0)
timeIn = now.replace(hour=8, minute=0, second=0, microsecond=0)
timeOut = now.replace(hour=17, minute=0, second=0, microsecond=0)


# if timeIn <= now :
#   attendance = {"_id": uuid.uuid4().hex,"email": "test","status": "asd","datetime": 'null'}

# print(attendance)
# # attendance = {"status": "Hadir"}
# attendance.update({
#                 "status": "Hadir",
#                 "datetime": now,
#             })
# print(attendance)
# attendance['datetime'] = now.strftime("%d/%m/%Y")
# print("date and time =", attendance['datetime'])
# print(now > timeIn and now < timeOut)
# print(yesterday)
# print(today < yesterday)
# print(today == yesterday)
# print(today > yesterday)
client = pymongo.MongoClient('localhost',27017)
db = client.user_login_system
data = db.attendance.find_one({"email": "person", "timeOut" : ""})


print(today.strftime("%d/%m/%Y") == data['timeIn'].strftime("%d/%m/%Y"))
