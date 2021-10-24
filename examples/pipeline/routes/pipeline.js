/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
const { default: axios } = require('axios');
var express = require('express');
var router = express.Router();
let logger = require('debug')('pipeline');

router.get('/', function (req, res, next) {
	debugger;
	let data = { ...req.query };

	if (data.count == null) {
		data.count = process.env.COUNT;
	}

	if (data.csv == null) {
		data.csv = process.env.CSV;
	}

	if (data.key == null) {
		data.key = process.env.KEY;
	}

    if (data.repeat == null) {
		data.repeat = process.env.REPEAT;
	}

	let p = {
		url: process.env.TARGET,
		method: 'POST',
		data: data
	};
	logger(p);

	debugger;
	axios(p)
		.then((r) => {
			logger(r.data);
			res.json(r.data);
		})
		.catch((err) => {
			logger(err);
			res.send(err);
		});
});

module.exports = router;
