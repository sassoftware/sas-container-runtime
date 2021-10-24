/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

let logger = require('debug')('persist');
let redis = require('redis');


module.exports = async function idbRedisWrite (invals) {

	if( process.env.REDIS_HOST === 'mock') {
		return 'done';
	}
	let { createClient } = redis;
	let key = `${invals.controls.key}:${invals.controls.group}_${invals.controls.recordNo}`;
	let client = createClient(process.env.REDIS_PORT,process.env.REDIS_HOST);
	client.on('error', (err) => {
		logger('Redis Client Error', err);
		throw 'no client'
	});
	
	debugger;
	logger('Writing to redis');
	logger(JSON.stringify(invals));
	client.set(key, JSON.stringify(invals), (err, r) => {
		logger('Return status from write ', r);
		client.get(key, (err, t) => {
			logger('Reading back the data');
			logger(t);
		});
	});

	return 'done';
}

