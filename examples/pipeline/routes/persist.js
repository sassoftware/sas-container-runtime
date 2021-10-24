/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
let idbRedisWrite = require('../lib/idbRedisWrite.js');
let logger = require('debug')('persist');

router.post('/', function (req, res, next) {
	logger('===================================================');
	idbRedisWrite(req.body)
		.then((_r) => res.sendStatus(204))
		.catch((_err) => {
			res.sendStatus(404);
		});
});

module.exports = router;
