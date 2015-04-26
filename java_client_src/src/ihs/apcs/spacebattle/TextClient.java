package ihs.apcs.spacebattle;

import ihs.apcs.spacebattle.commands.*;
import ihs.apcs.spacebattle.networking.*;
import ihs.apcs.spacebattle.util.StringStringMap;

import java.util.*;
import java.io.*;
import java.text.*;
import java.net.*;

/**
 * Simple, text-based test client for SpaceBattle game for IHS AP CS 2012.
 * @author Brett Wortzman
 *
 */
public class TextClient implements Client {
	private PrintStream logStream;
	private final boolean LOGGING = true;
	
	private int netId;
	private int shipId = -1;
	private MwnpListener listener;
	private MwnpMessenger messenger;
	private Spaceship ship;
	
	private boolean disconnected = false;
	
	private String shipSuffix = "";
	
	public TextClient() throws FileNotFoundException {
		logStream = new PrintStream("client.log");
	}
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		TextClient client = new TextClient();
		try {
			// Add disconnect hook
			Runtime.getRuntime().addShutdownHook(new ShutdownHook(client));

			// Connect to server
			System.out.println("Connecting to " + args[0]);
			client.logMessage("Connecting to server...");
			Socket server = new Socket(args[0], args.length >= 3 ? Integer.parseInt(args[2]) : 2012);
			
			// Start listening for messages
			client.logMessage("Starting listener...");
			client.listener = new MwnpListener(client, server, "Listener Thead");
			client.listener.start();
			
			// Start sending messages
			client.logMessage("Starting messenger...");
			client.messenger = new MwnpMessenger(client, server, "Messenger Thread");
			client.messenger.start();
			
			// Create ship
			Class<?> shipType = Class.forName(args[1]);
			client.logMessage("Creating new " + shipType.getName());
			client.ship = (Spaceship)shipType.getConstructor().newInstance();
			
			System.out.println(args.length);
			System.out.println(Arrays.toString(args));
			if (args.length > 3) {
				System.out.println("Adding suffix " + args[3]);
				client.shipSuffix = args[3];
			}
			
			// Wait for termination command
			System.out.println("Type QUIT to disconnect from server and end program");
			Scanner kb = new Scanner(System.in);
			while (kb.hasNextLine() && !kb.nextLine().equalsIgnoreCase("QUIT"));
			kb.close();
		} catch (IOException ex) {
			System.err.println("Server connection failed.");
			System.err.println(ex.getMessage());
			ex.printStackTrace();
		} catch (ClassCastException ex) {
			System.err.println("Specified ship type does not implement Spaceship.");
			System.err.println(ex.getMessage());
		} catch (ClassNotFoundException ex) {
			System.err.println("Specified ship type not found.");
			System.err.println(ex.getMessage());
		} catch (Exception ex) {
			System.err.println(ex.getMessage());
			ex.printStackTrace();
		} finally {
			client.disconnect();
		}
	}
	
	/**
	 * Reads a network message and takes appropriate action. 
	 * @param msg the message received from the network
	 * @throws IllegalAccessException 
	 * @throws IllegalArgumentException 
	 */
	public <T> void parseMessage(MwnpMessage msg) throws IOException, IllegalArgumentException, IllegalAccessException {
		if (msg.getCommand().equals("MWNL2_ASSIGNMENT")) {
			MwnpMessage dMsg = (MwnpMessage)msg;
			this.netId = ((Double)(dMsg.getData())).intValue();
		} else if (msg.getCommand().equals("MWNL2_AC")) {
			System.err.println("Already connected from this IP address.  Exiting...");
			System.exit(1);
		} else if (msg.getCommand().equals("REQUEST")) {
			StringStringMap map = (StringStringMap)msg.getData();
			int numImages = Integer.parseInt(map.get("IMAGELENGTH"));
			int width = Integer.parseInt(map.get("WORLDWIDTH"));
			int height = Integer.parseInt(map.get("WORLDHEIGHT"));
			// map.get("GAMENAME")
			
			RegistrationData data = ship.registerShip(numImages, width, height);
			data = new RegistrationData(data.getName() + shipSuffix, data.getColor(), data.getImage());
			
			MwnpMessage response = new MwnpMessage(new int[]{netId, 0}, data);
			messenger.sendMessage(response);
		} else if (msg.getCommand().equals("ENV")) {
			Environment env = (Environment)msg.getData();

			// check for death
			int currShipId = env.getShipStatus().getId();
			if (shipId == -1) {
				shipId = currShipId;
			}
			
			if (shipId != currShipId) {
				// new id means ship has died; inform ship
				ship.shipDestroyed();
				shipId = currShipId;
			}
			
			ShipCommand cmd = ship.getNextCommand(env);
			if (cmd == null) {
				cmd = new IdleCommand(0.1);
			} else if (cmd instanceof SelfDestructCommand) {
				disconnect();
			} else {
				MwnpMessage response = new MwnpMessage(new int[]{netId, 0}, cmd);
				messenger.sendMessage(response);
			}
		} else if (msg.getCommand().equals("ERROR")) {
			logMessage(msg.getData().toString());
			System.err.println(msg.getData().toString());
			//ship.processError((ErrorData)msg.getData());
		} else if (msg.getCommand().equals("MWNL2_DISCONNECT")) {
			this.disconnect();
		}
	}
	
	public void disconnect() throws IOException {
		System.out.println("Attempting to disconnect...");
		if (!disconnected) {
			logMessage("Sending disconnect message...");
			MwnpMessage disconnect = new MwnpMessage(new int[]{netId, 0}, "MWNL2_DISCONNECT", null);
			messenger.sendMessage(disconnect);
			logMessage("Ending listener...");
			listener.end();
			logMessage("Ending messenger...");
			messenger.end();
		}
		disconnected = true;
		System.out.println("Disconnect complete.");
	}
	
	public void logMessage(String message) {
		if (LOGGING) {
			Calendar now = Calendar.getInstance();
			logStream.print("LOG: ");
			logStream.print(DateFormat.getDateTimeInstance().format(now.getTime()));
			logStream.print(": ");
			logStream.println(message);
		}
	}
}
