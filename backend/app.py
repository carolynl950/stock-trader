"""
Flask backend for executing user-defined trading strategies.

Educational project – paper trading only.
User code execution is not sandboxed.
"""


from flask import Flask, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, storage, auth
import json
import os
import datetime
import pytz
app = Flask(__name__)
CORS(app)
f = open('sample.json')
file_text = json.load(f)
uid = file_text["name"]

cred = credentials.Certificate("key.json")
initialize_app(cred, {'storageBucket': 'test-cac6d.appspot.com'})

bucket = storage.bucket()
page = auth.list_users()

uid_list = {}
for user in page.users:
  uid_list[user.uid] = datetime.datetime(datetime.MINYEAR,
                                         1,
                                         1,
                                         0,
                                         0,
                                         0,
                                         0,
                                         tzinfo=pytz.utc)

file_holder = {}
for user in page.users:
  file_holder[user.uid] = ""
# use this to manually upload a file
@app.route('/upload')
def upload_file():
  # Put your local file path
  fileName = "0.py"
  blob = bucket.blob(uid + '/')
  blob.upload_from_filename(fileName)

  print("File has been uploaded.")
  return jsonify(file_text)
@app.route('/run')
def download_blob():
  target = bucket.list_blobs()
  blobList = list(iter(target))
  for x in range(len(blobList)):
    # print("File number: " + str(x))
    for name in uid_list:
      if blobList[x].name.find(name) >= 0:
        print("User found!\n-----------------\n", blobList[x].time_created,
              "\n-----------------")
        # check if date in dictionary is earlier than the current date we find
        if uid_list[name] < blobList[x].time_created:
          uid_list[name] = blobList[x].time_created
          file_holder[name] = blobList[x]
          break
      else:
        print("Names do not match. Current UID:", name,
              "\n-----------------\nCurrent file path:", blobList[x].name,
              "\n-----------------")

  for file in file_holder:
    if isinstance(file_holder[file], str) == False:
      try:
        file_holder[file].download_to_filename(str(file) + ".py")
        exec(open(str(file) + ".py").read())
      except:
        print("Error while reading file!")
    else:
      print("Blob not found!", file)

  # dates are returned as GMT
  return jsonify(uid_list)


if __name__ == '__main__':
  print(os.listdir("."))
  app.run(host='0.0.0.0')

f.close()




