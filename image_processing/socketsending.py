import socketio
import base64

HOST = "192.168.31.55"
PORT = 3000

sio = socketio.Client()
sio.connect('http://192.168.31.55:3000')
# while True:
with open("photo_2019-09-03_13-51-58.png", "rb") as image:
    encoded_string = base64.b64encode(image.read())
# print(str(encoded_string))
encoded_string = 'data:image/jpeg;base64,'+str(encoded_string)[2:-1]
print(encoded_string)
sio.emit('Camera', encoded_string)

