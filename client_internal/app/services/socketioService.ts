import * as io from "socket.io-client";
import { EventEmitter, Input, Output } from "@angular/core";

// Listen to channels of data passed from node_midtier
export class SocketIOService {
    private socket: SocketIOClient.Socket;

    public environment: IEnvironment;
    public request: IRequest;

    public haveData: (() => void);

    public init(log: HTMLElement) {
        this.socket = io.connect('http://localhost:2017');
        
        this.socket.on('log', function(data) { 
            console.log(data);
            log.innerHTML += "<p>" + data + "</p>";
        }); // listen to the event

        this.socket.on('cmd', function(data) { 
            let obj = JSON.parse(data);
            //console.log(obj);
            log.innerHTML += "<p>" + data + "</p>";
        }); // listen to the event

        this.socket.on('request', (data) => {
            // TODO: What if we miss this data???
            this.request = JSON.parse(data);
        });

        this.socket.on('env', (data) => { 
            //String.fromCharCode.apply(null, new Uint8Array(data))
            this.environment = JSON.parse(data);

            if (this.haveData)
            {
                this.haveData();
                this.haveData = null; // TODO: Clean-up this event structure.
            }
            //console.log(this.environment);
            //document.getElementById('console').innerHTML += "<p>" + data + "</p>";
        }); // listen to the event
    }
}