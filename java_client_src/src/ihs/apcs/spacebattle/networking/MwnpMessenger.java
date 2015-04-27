package ihs.apcs.spacebattle.networking;

import java.io.*;
import java.net.Socket;

public class MwnpMessenger extends Thread {
	private Client client;
	private OutputStreamWriter outStream;
	private Socket sock;
	
	private final boolean LOGGING = true;
	private PrintStream logStream;
	

	public MwnpMessenger(Client client, Socket sock, String name) throws IOException {
		super(name);
		this.client = client;
		this.sock = sock;
		outStream = new OutputStreamWriter(sock.getOutputStream());
		
		logStream = new PrintStream("messenger.log");
		//logStream = System.out;
	}
	
	public void run() { }
	
	public void end() throws IOException { 
		client.logMessage("Messenger ending...");
		if (!sock.isClosed()) {
			sock.shutdownOutput();
			sock.close();
		}
	}
	
	public void sendMessage(MwnpMessage msg) throws IOException {
		if (!sock.isClosed() && !sock.isOutputShutdown()) {
			String msgString = msg.toJsonString();
			outStream.write(msgString, 0, msgString.length());
			outStream.flush();
			
			if (LOGGING)
				printMessage(msg);
		}
	}
	
	private void printMessage(MwnpMessage message) {
		logStream.printf("Message sent from %d to %d - \r\n", message.getSenderId(), message.getReceiverId());
		logStream.printf("  %s(%s)\r\n", message.getCommand(), message.getData());
	}
}
