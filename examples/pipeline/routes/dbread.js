/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
let idbRedisRead = require('../lib/idbRedisRead.js');
let logger = require('debug')('pipeline');
/* GET users listing. */

router.get('/', function (req, res) {
	debugger;
	let { key } = req.query;
	logger(key);
	idbRedisRead(key)
		.then((r) => {
			debugger;
			res.json(r);
		})
		.catch((err) => {
			logger(err);
			res.json({ status: 'error' });
		});
});

module.exports = router;
