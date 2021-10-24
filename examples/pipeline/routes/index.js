/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
var express = require('express');
var router = express.Router();
var path = require('path');
/* GET home page. */
router.get('/', function (req, res, next) {
	res.sendFile(path.join(__dirname, '/Public/index.html'));
});

module.exports = router;
