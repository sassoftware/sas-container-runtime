/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let axios = require('axios');

let p = {
	url: 'http://localhost:8080/pipeline',
	method: 'GET',
	params: {
		key: 'hl',
		csv: './hmeq.csv',
		count: 10,
		repeat: 10
	},
};
debugger;
axios(p)
    .then(r => { debugger; console.log(r.data); process.exit(0); })
    .catch(e => console.log(e));

