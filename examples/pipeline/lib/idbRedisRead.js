/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

let logger = require('debug')('db');
let redis = require('redis');


module.exports = async function idbRedisRead (key) {
	let { createClient } = redis;
	let client = createClient(process.env.REDIS_PORT,process.env.REDIS_HOST);
	client.on('error', (err) => {
		logger('Redis Client Error', err);
		throw 'no client'
	});
	
	debugger;
		
	let r = await read1(client, key);
	console.log(r);
	return r;
}

function read1 (client, key) {
	return new Promise((resolve, reject) => {
		client.get(key, (err, t) => {
			logger('Reading back the data');
			logger(t);
			let tj = JSON.parse(t);
			return (err) ? reject(err) : resolve(tj);
		});

	})
}
