// __author__ = 'Michael Uschmann / MuS'
// __date__ = 'Copyright $Oct 25, 2018 11:00:00 AM$'
// __version__ = '0.1.1'

// get config arguments
var remote_user = process.argv[2],
    locale = 'en-GB',
    proxy_port = process.argv[3],
    connect_from = process.argv[4],
    splunk_port = '8000';

// fixed variables - HaHA!
var myPath = '/opt/splunk/etc/apps/TA-EDFS/bin/'
    http = require('http'),
    httpProxy = require('http-proxy');
    // https = require('https'),
    // fs = require('fs');

// Create a proxy server with custom application logic
var proxy = httpProxy.createProxyServer({
    target: 'http://127.0.0.1:' + splunk_port
});

// Modify the header to allow the user to login
proxy.on('proxyReq', function(proxyReq, req, res, options) {
  proxyReq.setHeader('Accept-Language', locale);
  proxyReq.setHeader('REMOTE_USER', remote_user);
});

var server = http.createServer(function(req, res) {
  // check if the client IP is allowed to connect
  var epoch = (new Date).getTime();
  var client_ip = req.connection.remoteAddress.replace(/^[:f]+/, '');
  if (!(client_ip == connect_from )) {
     console.log("_time=\"" + epoch + "\" clientIp=\"" + req.connection.remoteAddress.replace(/^[:f]+/, '') + "\" proxy=\"" + req.headers.host + "\" message=\"Emergency, paging Dr. Beat! Someone is connecting from the wrong IP!!!\" url=\"" + req.url + "\"");
     return;
  }

  // check if we have a search request in the url
  var search_check = req.url.match(/(\/search\/jobs)/);

  // check for HTTP POST that is NOT a search, and exit!
  var epoch = (new Date).getTime();
  if (req.method == 'POST' && search_check == null ) {
     console.log("_time=\"" + epoch + "\" user=\"" + remote_user + "\" clientIp=\"" + req.connection.remoteAddress.replace(/^[:f]+/, '') + "\" proxy=\"" + req.headers.host + "\" message=\"Emergency, paging Dr. Beat! Someone is using a POST!!!\" url=\"" + req.url + "\"");
     return;
  }

  // allow connection and proxy it to Splunk
  var epoch = (new Date).getTime();
  console.log(remote_user);
  console.log("_time=\"" + epoch + "\" user=\"" + remote_user + "\" clientIp=\"" + req.connection.remoteAddress.replace(/^[:f]+/, '') + "\" proxy=\"" + req.headers.host + "\" url=\"" + req.url + "\"" );
  proxy.web(req, res);
});

var start_epoch = (new Date).getTime();
console.log("_time=" + start_epoch + " message=\"Starting Dashboard proxy on port " + proxy_port + "\"")
server.listen(proxy_port);
