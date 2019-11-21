var SocketIO = require('socket.io');
var moment = require('moment');
var Token = require('./models/Token');
var admin = require('firebase-admin');
var serviceAccount = require('./fir-storage-sdk.json');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

module.exports = (server) => {
    var io = SocketIO(server);
    
    console.log("소켓IO 서버 오픈");

    io.on('connection', function (socket) {
        console.log("유저가 접속하였습니다 :: ", moment().format("YYYY-MM-DD HH:mm:ss"));

        socket.on('Token', function (data) {
            var tokens = new Token();
            tokens.code = data;

            Token.findOne({ code: data } , function (err, token) {
                if (err) {
                    console.error(err);
                }
                if(token){
                    io.emit('DoorMsg', "이미 등록된 사용자입니다");
                }
                else{
                    tokens.save(function (err) {
                        if (err) {
                            console.error(err);
                        }
                        io.emit('DoorMsg', "기기가 등록되었습니다");
                    });
                }
                
            });
        });
        
        socket.on('Camera', function(img){
            io.emit('Image',img);
        });

        socket.on('MobileMsg', function (data) {
            console.log(data);
            io.emit('MobileMsg', data);
        });

        socket.on('DoorMsg', function (data) {
            var payload = {
                notification: {
                    title: "SMART DOOR",
                    body: data + " 이(가) 방문했습니다"
                }
            };
            Token.find(function (err, tokens) {
                if (err) {
                    console.log(err);
                }
                var code = [];
                for (let i = 0; i < tokens.length; i++) {
                    code.push(tokens[i].code);
                }
                admin.messaging().sendToDevice(code, payload)
                    .then(function (response) {
                        console.log(response);
                    })
                    .catch(function (err) {
                        console.log(err);
                    });
            })

            io.emit('DoorMsg', data);
        });
    });
};