/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let redis = require('redis');
let { createClient } = redis;
let logger = require('debug')('pipeline');
let client = createClient(6379,'localhost');
client.on('error', (err) => console.log('Redis Client Error', err));

let keys = '*';
debugger;
runList(client, keys)
    .then(r => { console.log(r); process.exit(0) })
    .catch(err => console.log(err));

async function runList(client, keys) {

    let keyArray = [ keys ];
    if (keys === '*') {
        keyArray = await getKeys(client);
    }
    logger(keyArray);

    for (let i = 0; i < keyArray.length; i++){
        let val = await getValue(client, keyArray[ i ]);
        logger('==========', val);
    }

    return 'done';

}

function getKeys(client) {
	return new Promise((resolve, reject) => {
		client.keys('*', (err, t) => {
			logger(t);
			console.log(t);
			return err ? reject(err) : resolve(t);
		});
	});
}
function getValue (client, key) {
    return new Promise((resolve, reject) => {
        client.get(key, (err, t) => {
            logger('Reading back the data ' , key);
            return (err) ? reject(err) : resolve(t);
        });

 
    })
}

/*
client.keys('*', (err, r) => {
    console.log('find ', r);
    console.log(err);
    r.map(k => {
        client.get(k, (err, r) => {
            console.log(r);
        })
    })
})
*/