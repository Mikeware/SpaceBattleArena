import * as httpserver from 'http-server';
import * as net from 'net';
import * as http from 'http';
import * as socketio from 'socket.io';
import * as process from 'process';

// This module serves three purposes
// 1) Create a web-server to host browser portal
// 2) Act as man-in-middle between client & server to intercept communications
// 3) Pass communications up to the browser layer

// Serve Pages to make connection from Browser Easier
httpserver.createServer().listen(80, '127.0.0.1', () => {
    console.log("Web Server Running");
});

// Server Socket Channel to Web Browser
var sioserver = http.createServer();
var io: SocketIO.Server = socketio(sioserver);
io.on('connection', function(client){
  client.on('event', function(data){});
  client.on('disconnect', function(){});
});
sioserver.listen(2017);

// Look for Local Client Connection from Program
var server = net.createServer(function(socket) {
    // Create a Connection to Actual SBA Server
    var msg = "Client Connected from " + socket.localAddress + ":" + socket.localPort;
    console.log(msg);
    io.emit('log', msg);

    var client = new net.Socket();
    client.connect(2016, '127.0.0.1', () => {
        client.setNoDelay(true);
        io.emit('log', 'Connected to Server');
        console.log('Connected to Server');
    });

    client.on('data', function(data) {
        //console.log('Client Received: ' + data);
        let s: string = String.fromCharCode.apply(null, data);
        s = s.substr(s.indexOf('{'));
        io.emit('env', s); 

        socket.write(data);
    });

    //socket.write('Echo server\r\n');
    //socket.pipe(socket);
    socket.on('data', function(data) {
        console.log('Sending to Server: ' + data);
        let s: string = String.fromCharCode.apply(null, data);
        s = s.substr(s.indexOf('[', 10));
        io.emit('cmd', s);
        client.write(data); // forward to server
    })

    socket.on('close', function() {
        console.log('Server Connection closed');
    });

    socket.on('error', function(err) {
        io.emit('log', "Error: " + err);
    });

    client.on('close', function() {
        console.log('Client Connection closed');
    });

    client.on('error', function(err) {
        io.emit('log', "Error: " + err);
    })
});

server.listen(2012, '127.0.0.1');

process.on('uncaughtException', function (err) {
    console.log("Handled Error");
    console.error(err);
});
