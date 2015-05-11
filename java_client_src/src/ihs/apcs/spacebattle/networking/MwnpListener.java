package ihs.apcs.spacebattle.networking;


import java.net.*;
import java.io.*;

public class MwnpListener extends Thread {
	private InputStream inStream;
	private Socket sock;
	private Client client;
	private boolean running;
	
	private final boolean LOGGING = true;
	private PrintStream logStream;
	
	public MwnpListener(Client client, Socket sock, String name) throws IOException {
		super(name);
		this.client = client;
		this.sock = sock;
		inStream = sock.getInputStream();
		running = true;
		
		logStream = new PrintStream("listener.log");
		//logStream = System.out;
	}
	
	public void run() {
		while (running) {
			try {
				int msgSize = getMessageLength();
				if (msgSize == -1) 
					return;
				
				MwnpMessage msg = getMessage(msgSize);
				
				if (msg == null)
					return;
				
				client.parseMessage(msg);
	
				if (LOGGING)
					printMessage(msg);				
			} catch (IOException ex) {
				System.err.println("Server read error...");
				System.err.println(ex.getMessage());
				ex.printStackTrace();
			} catch (IllegalArgumentException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	public void end() throws IOException {
		client.logMessage("Listener ending...");
		if (!sock.isClosed()) {
			sock.shutdownInput();
			sock.close();
		}
		running = false;
	}
	
	/**
	 * Find the number of bytes in the incoming message.
	 * Reads until a '[' is hit, then parses the resulting bytes as an integer
	 *   which indicates the message length.
	 * The '[' will be consumed, and will need to be replaced when the message is 
	 *   actually read.
	 * @return the number of bytes in the next message on the stream.
	 * @throws IOException - if a read error occurs
	 */
	private int getMessageLength() throws IOException {
		StringBuilder builder = new StringBuilder();
		int currByte = -1;
		try {
			while (!sock.isClosed()) {
				currByte = inStream.read(); 
				
				if (currByte != -1 && currByte != '[')
					builder.append((char)currByte);
				else
					break;
			}
		} catch (SocketException ex) {
			// disconnected while waiting for message... carry on
		}

		if (sock.isClosed() || currByte == -1) 
			return -1;
		return(Integer.parseInt(builder.toString()));
	}
	
	/**
	 * Reads a MWNP message of the given length from the input stream.
	 * Since the first '[' will have been consumed finding the length, that
	 *   character is added to the front of the message before reading.
	 * @param length the number of bytes to read
	 * @return the message
	 * @throws IOException - if a read error occurs
	 */
	private MwnpMessage getMessage(int length) throws IOException {
		StringBuilder builder = new StringBuilder("[");
		for (int i = 0; i < length - 1; i++) {
			int currByte = inStream.read();
			if (currByte == -1)
				return null;
			
			builder.append((char)currByte);
		}
		String message = builder.toString();
		
		return MwnpMessage.parseMessage(message);
	}
	
	private void printMessage(MwnpMessage message) {
		logStream.printf("Message received from %s intended for %s - \r\n", message.getSenderId(), message.getReceiverId());
		logStream.printf("  %s(%s)\r\n", message.getCommand(), message.getData());
	}
}
