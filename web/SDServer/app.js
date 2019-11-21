var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var Mongodb = require('./MongoDB');
var cors = require('cors');

var indexRouter = require('./routes/index');
var ResidentRouter = require('./routes/Resident');

var app = express();

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

Mongodb();

app.use('/', indexRouter);
app.use('/residents', ResidentRouter);

module.exports = app;
