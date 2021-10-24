/*
 * Copyright © 2021, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
const request = require('supertest');
const app = require('../app');

describe('App', function() {
  it('has the default page', function(done) {
    request(app)
      .get('/')
      .expect(/Welcome to Express/, done);
  });
}); 
describe('App', function () {
	it('post call', function (done) {
		request(app)
			.post('/score', {a:1, b:2})
			.expect(/posted/, done);
	});
}); 