import * as io from "socket.io-client";

export class SocketIOService {
    private socket: SocketIOClient.Socket;

    public init() {
        this.socket = io.connect('http://localhost:2017');
        
        this.socket.on('log', function(data) { 
            console.log(data);
            document.getElementById('console').innerHTML += "<p>" + data + "</p>";
        }); // listen to the event

        this.socket.on('cmd', function(data) { 
            console.log(data);
            document.getElementById('console').innerHTML += "<p>" + data + "</p>";
        }); // listen to the event

        this.socket.on('env', function(data) { 
            //String.fromCharCode.apply(null, new Uint8Array(data))
            console.log(data);
            //document.getElementById('console').innerHTML += "<p>" + data + "</p>";
        }); // listen to the event
    }
}