import * as httpserver from 'http-server';
import * as net from 'net';
import * as http from 'http';
import * as socketio from 'socket.io';

// Server Pages to make connection from Browser Easier
httpserver.createServer().listen(80, '127.0.0.1', () => {
    console.log("Server Running");
});

// Server Socket Channel to Web Browser
var sioserver = http.createServer();
var io: http.Server = socketio(sioserver);
io.on('connection', function(client){
  client.on('event', function(data){});
  client.on('disconnect', function(){});
});
sioserver.listen(2017);

// Look for Local Client Connection from Program
var server = net.createServer(function(socket) {
    // Create a Connection to Actual SBA Server
    console.log("Received Connection From Client from " + socket.localAddress + ":" + socket.localPort);

    io.emit('log', "Client Connected");

    //socket.write('Echo server\r\n');
    //socket.pipe(socket);
    socket.on('data', function(data) {
        console.log('Server Receieved: ' + data);        
        io.emit("log", data);
    })

    socket.on('close', function() {
        console.log('Server Connection closed');
    });
});

server.listen(2012, '127.0.0.1');

/*
process.on('uncaughtException', function (err) {
            console.log("Handled Error");
            console.error(err);
        });

        var client = new net.Socket();
        client.connect(39999, '127.0.0.1', () => {
            client.setNoDelay(true);
            console.log('Connected');
            this.status.text = "$(plug) Connected to TTS";
            
            client.write(JSON.stringify(new ClientGetScripts()));
        });

        var curdata = "";
        client.on('data', function(data) {
            console.log('Client Received: ' + data);
            //window.showInformationMessage("Received Global.lua from TTS");
            //client.destroy(); // kill client after server's response
            curdata += data;
            try {
                var ourdata = <TabletopSimulatorMessage>JSON.parse(curdata);
                if (ourdata.messageID == 0)
                {
                    var message = <ServerReceiveScripts>(ourdata);
                    var settings = setmanager.GetSettings();

                    // Create output folder if it doesn't exist yet.
                    if (!fs.existsSync(workspace.rootPath + settings.defaultScriptPath))
                    {
                        fs.mkdirSync(workspace.rootPath + settings.defaultScriptPath);
                    }

                    message.scriptStates.forEach(script => {
                        var filename: string;
                        if (settings.scriptMapping.hasOwnProperty(script.guid))
                        {
                            // Existing Script/Mapping
                            filename = workspace.rootPath + settings.defaultScriptPath + settings.scriptMapping[script.guid];
                        } else {
                            // New Script
                            filename = workspace.rootPath + settings.defaultScriptPath + script.name + ' - ' + script.guid + '.lua';
                            window.showInformationMessage("TTS - New Script Created: " + filename);
                        }
                        fs.writeFileSync(filename, script.script);
                        commands.executeCommand('vscode.open', Uri.file(filename));
                    });                    
                }                
            } catch (err) {
                console.log("Not Ready: " + err);
            }	
        });

        client.on('close', function() {
            console.log('Client Connection closed');
        });

        client.on('error', function(err) {
            window.showErrorMessage("Could not connect to TTS: " + err);
        })*/