var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
let redis = require('redis');


var indexRouter = require('./routes/index');
var dbRouter = require('./routes/db');
var scrWrapperRouter = require('./routes/scrwrapper');
var dbConsoleRouter = require('./routes/dbconsole');
var persistRouter = require('./routes/persist');
var pipelineRouter = require('./routes/pipeline');
var dbReadRouter = require('./routes/dbread');
require('dotenv').config();

var app = express();
app.use(express.json());


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());

/*
if (process.env.REDIS_HOST != null) {
  let { createClient } = redis;
  let client = createClient({ port: process.env.REDIS_PORT, host: process.env.REDIS_HOST });
  app.locals.redisClient = client;
  console.log('client', client);
}
*/
app.locals.redisClient = 'placeholder';
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/db', dbRouter);
app.use('/scrwrapper', scrWrapperRouter);
app.use('/pipeline', pipelineRouter);
app.use('/dbconsole', dbConsoleRouter);
app.use('/persist', persistRouter);
app.use('/find', dbReadRouter);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
