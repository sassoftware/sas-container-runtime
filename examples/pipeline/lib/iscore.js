/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let axios = require('axios');
let debug = require('debug');
let logger = debug('scrwrapper');

module.exports = async function iscore (url, invals, drop) {
	if (url === 'mock' ) {
		return { status: 'done' };
	} else {
		logger(invals);
		let data = [];
        for (let key in invals.data) {
            if (drop.indexOf(key) === -1) {
                let value = invals.data[ key ];
                if (value.length === 0) {
                    value = ' ';
                }
                let d = { name: key };
                d.value = (value === null || isNaN(value) === true) ? value : Number(value);
                data.push(d);
            }
		}
	
		let p = {
			url: url,
			method: 'POST',
			data: {inputs: data}
		};
		logger('processing record with ', url);

		let o = {
			controls: invals.controls,
			inputs: data,
		};

		try {
			let r = await axios(p);
			o.result = r.data;
			logger('=======================================================Successful scoring');
			logger(o);
			return o;
		}
		catch (err) {
			logger('=======================================================Failed scoring');
			o.outputs = { error: true };
			return o;
		}
	}
};
