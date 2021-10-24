
/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let axios = require('axios');
let csvtojson = require('csvtojson');
let debug = require('debug');
let logger = debug('db');
module.exports = async function idbCsv (url, userInfo) {
    logger(userInfo);
    let { csv, count, repeat} = userInfo;
    let rows = await csvtojson().fromFile(csv);
    count = (count == null) ? 1 : (count === 'all') ? rows.length : count;
    repeat = (repeat == null) ? 1 : repeat;
    logger(`rows: ${count}`);
    logger(`repeat: ${repeat}`);

    let controls = { ...userInfo };

    for (let j = 0; j < repeat; j++) {
        for (let i = 0; i < count; i++) {
            data = rows[ i ];
            controls.recordNo = i;
            controls.group    = j;
            logger('Sending record ', i);
            let d = {
                controls,
                data
            }
            runSingle(url, d, i, ((err, r) => {
            }));

        }
    }

    return {
		status: `Last record sent downstream`,
		userInfo,
		target: url,
	};
    
}

function runSingle (url, data, n,  cb) {
    if (url == 'mock') {
        cb(null, 'done');
    } else {
        let config = {
            url: url,
            method: 'POST',
            data: data
        }
        logger(data);
        axios(config)
            .then((r) => {
                logger(`Status: OK, Record: ${n}, From: ${url}` );
                cb(null, r);
            })
            .catch((e) => {
    
                logger(`Status: Error, Record: ${n}, status: ${e}, From: ${url}`);
                cb(e)
            });
    }
}