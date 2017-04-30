import * as io from "socket.io-client";
import { EventEmitter, Input, Output } from "@angular/core";

// Listen to channels of data passed from node_midtier
export class SocketIOService {
    private socket: SocketIOClient.Socket;

    public environment: IEnvironment;
    public request: IRequest;

    public haveData: (() => void);

    private logDiv: HTMLElement;

    private log(text: string) {
        this.logDiv.innerHTML = "<p class='green'>" + this.date() + text + "</p>" + this.logDiv.innerHTML;
    }

    private cmd(text: string) {
        this.logDiv.innerHTML = "<p>" + this.date() + text + "</p>" + this.logDiv.innerHTML;
    }

    private date(): string {
        let t = new Date();
        let s = t.toLocaleTimeString();
        let m = ("000" + t.getMilliseconds()).slice(-3);
        return "<span class='time'>" + s.substr(0, s.length-3) + "." + m + "</span> - ";
    }

    public init(log: HTMLElement) {
        this.logDiv = log;
        this.socket = io.connect('http://localhost:2017');
        
        this.socket.on('log', (data) => { 
            console.log(data);
            this.log(data);
        }); // listen to the event

        this.socket.on('cmd', (data) => { 
            let obj = JSON.parse(data);
            //console.log(obj);
            this.cmd(data);
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