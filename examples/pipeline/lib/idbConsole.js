/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

let debug = require('debug');
let logger = debug('dbconsole');
module.exports = async function idbConsole (invals) {
	if (process.env.DETAILS === 'long') {
		logger('==========');
		logger(JSON.stringify(invals));
		logger('==============');
		return 'done';
	} else if (process.env.DETAILS === 'short') {
		logger('no details');
		return 'done';
	} else {
		return 'done';
	}
};
