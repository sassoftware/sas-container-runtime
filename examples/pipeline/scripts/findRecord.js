/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let axios = require('axios');
debugger;
console.log(process.argv);
let filter = process.argv[ 2 ];
let p = {
    url: 'http://localhost:8080/find',
    method: 'GET',
    params: {
        key: filter
    }
}
console.log(p);
debugger;

axios(p)
    .then(r => { debugger; console.log(JSON.stringify(r.data, null,4)); process.exit(0); })
    .catch(e => console.log(e));

