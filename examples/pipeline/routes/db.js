/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
let idbCsv = require('../lib/idbCsv.js');
let logger = require('debug')('db');
/* GET users listing. */

router.post('/', function (req, res) {
	debugger;
	logger(req.body);
	idbCsv(process.env.TARGET, req.body)
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
