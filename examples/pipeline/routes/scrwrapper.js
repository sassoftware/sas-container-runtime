/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
let iscore = require('../lib/iscore.js');
let logger = require('debug')('scrwrapper')
const itarget = require('../lib/itarget.js');

router.post('/', function (req, res, next) {
	logger('============================================');
	
	iscore(process.env.SCR_URL, req.body, process.env.DROP)
		.then (score => itarget(process.env.TARGET, score))
		.then(() => res.sendStatus(204))
		.catch( (err) => {
			logger('Failed in accessing ', process.env.TARGET);
			res.sendStatus(400);
		});
})

module.exports = router;
