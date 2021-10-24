/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
let axios = require('axios');
let logger = require('debug')('scrwrapper');
module.exports = async function itarget (url, data) {
    if (url == null ||url == 'mock') {
        return { status: 'mock' };
    }
    let config = {
        url: url,
        method: 'POST',
        data : data
    }
    logger('Sending data to ', url)
    logger(data);
    await axios(config);
    logger('Succesful return from ', url)
    return true;
}