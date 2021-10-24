/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
let idbConsole = require('../lib/idbConsole.js');

router.post('/', function (req, res, next) {
	idbConsole(req.body)
		.then((r) => res.status(204))
		.catch((err) => {
			console.log(err);
			res.send(err);
		});
});

module.exports = router;
