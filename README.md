# Photoservice
Simple API for [Photosender](https://github.com/ashchuk/photosender) app

Hosted on [Openshift 2](https://www.openshift.com/). Used MongoDB 3.2 as storage.

To start on localhost just:
1. Install [MongoDB](https://www.mongodb.com/)>=3.2 on local machine
2. Start ```mongod``` in console
3. Excecute ```wsgi.py``` script

## Requirements

* pillow
* pymongo>=3.5.0
* tornado>3
* jsonpickle

## API reference
* /login - login, set cookies
* /logout - logout, clear cookies
* /registration - add new user
* /getuser - get registered user
* /getuseravatar - get base64 encoded user avatar
* /updateuser - change user's name or avatar
* /addphoto - add new photo
* /getrandomphoto - get random photo
* /getphoto - get photo by uid
* /getimage - get base64 encoded photo image
* /getphotos - get 10 random photos
