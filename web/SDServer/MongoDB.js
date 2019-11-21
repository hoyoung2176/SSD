const mongoose = require('mongoose');
var moment = require('moment');
const uri = "mongodb+srv://SmartDoorDB:oqMW81CaG2d8FL17@cluster0-3044t.mongodb.net/test?retryWrites=true&w=majority";

module.exports = () => {
  function connect() {
    mongoose.connect(uri,{ useNewUrlParser: true, useUnifiedTopology: true },
      function (error) {
        if (error) {
          console.error('mongodb connection error', error);
        }
        else {
          var time = moment().format("YYYY-MM-DD HH:mm:ss");
          console.log(time + " MongoDB Connected !!");
        }
      });
  }
  connect();
  mongoose.connection.on('disconnected', connect);
};

