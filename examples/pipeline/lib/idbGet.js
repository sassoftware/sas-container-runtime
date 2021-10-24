/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let redis = require('redis'); 
let debug = require('debug');
let logger = debug('dbget');

module.exports = async function idbGet () {
	let { createClient } = redis;
	let client = createClient(process.env.REDIS_PORT,process.env.REDIS_HOST);
	client.on('error', (err) => {
		console.log('Redis Client Error', err)
	});

	let keys = await getKeys();
	if (keys.length === 0) {
		return { records: [] };
	}
	let doc = [];
	for (let i = 0; i < keys.length; i++) {
		let r = await getRecord(keys[i]);
		doc.push(r);
		if (i === keys.length) { 		
	       return { records: doc };
		}
	}
	
	

};

function getKeys () {
	return new Promise((resolve, reject) => {
		client.keys('*', (err, r) => {
			if (err == null) {
				resolve(r);
			} else {
				reject(err);
			}
		})
	})
}
function getRecord(k) {
	return new Promise((resolve, reject) => {
		client.get('k', (err, r) => {
			console.log(r);
			if (err == null) {
				resolve(JSON.parse(r));
			} else {
				reject(err);
			}
		});
	});
	
}