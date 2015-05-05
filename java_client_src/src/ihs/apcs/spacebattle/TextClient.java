/**
 * Space Battle Arena is a Programming Game.
 *
 * Copyright (C) 2012-2015 Michael A. Hawker and Brett Wortzman
 *
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 * The full text of the license is available online: http://opensource.org/licenses/GPL-2.0
 */

package ihs.apcs.spacebattle;

import ihs.apcs.spacebattle.commands.*;
import ihs.apcs.spacebattle.networking.*;
import ihs.apcs.spacebattle.util.StringStringMap;

import java.util.*;
import java.io.*;
import java.text.*;
import java.lang.reflect.InvocationTargetException;
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
	private String shipClassname;
	private Spaceship<?> ship;	
	private Class<?> shipType;
	
	private boolean disconnected = false;
	
	private String shipSuffix = "";
	
	public TextClient(String classname) {
		try {
			logStream = new PrintStream("client.log");
		} catch (FileNotFoundException ex) {
			System.err.println("Could not write to 'client.log' file.");
		}
		shipClassname = classname;
	}
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) {
		if (args == null || args.length < 2)
		{		
			System.err.println("Invalid parameters. Require IP Address and Class Name.");
			return;
		}
		
		System.out.println("Loading Ship " + args[1]);
		TextClient client = new TextClient(args[1]);
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
						
			// Try and load ship
			client.shipType = Class.forName(client.shipClassname);
			client.logMessage("Creating new " + client.shipType.getName());			
			client.ship = (Spaceship<?>)client.shipType.getConstructor().newInstance();
			
			System.out.println(args.length);
			System.out.println(Arrays.toString(args));
			if (args.length > 3) {
				System.out.println("Adding suffix " + args[3]);
				client.shipSuffix = args[3];
			}
			
			// Wait for termination command
			System.out.println("Type QUIT to disconnect from server and end program");
			Scanner kb = new Scanner(System.in);
			// TODO: Be able to break-out of this loop and end program when the client receives a disconnect message
			while (kb.hasNextLine() && !kb.nextLine().equalsIgnoreCase("QUIT"));
			kb.close();
		} catch (IOException ex) {
			System.err.println("Server connection failed.");
			System.err.println(ex.getMessage());
			ex.printStackTrace();
		} catch (ClassCastException ex) {
			System.err.println("Specified ship type does not implement Spaceship.");
			System.err.println(ex.getMessage());
		} catch (Exception ex) {
			System.err.println(ex.getMessage());
			ex.printStackTrace();
		} finally {
			try {
				client.disconnect();
			} catch (IOException ex) {
				System.err.println("Error while disconnecting:");
				ex.printStackTrace(System.err);
			}
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

			MwnpMessage.RegisterGameType(map.get("GAMENAME"));			
						
			RegistrationData data = ship.registerShip(numImages, width, height);
			data = new RegistrationData(data.getName() + shipSuffix, data.getColor(), data.getImage());
			
			MwnpMessage response = new MwnpMessage(new Integer[]{netId, 0}, data);
			messenger.sendMessage(response);
		} else if (msg.getCommand().equals("ENV")) {
			Environment<?> env = (Environment<?>)msg.getData();

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
			
			ShipCommand cmd = null;
			try {
				// Need to invoke through reflection as compiler doesn't know what type of Environment is here
				cmd = (ShipCommand)shipType.getMethod("getNextCommand", Environment.class).invoke(ship, env);
			} catch (InvocationTargetException | NoSuchMethodException
					| SecurityException ex) {
				System.err.println("Error Invoking getNextCommand:");
				System.err.println(ex.getMessage());
				ex.printStackTrace(System.err);
			}
			if (cmd == null) {
				cmd = new IdleCommand(0.1);
			} else if (cmd instanceof SelfDestructCommand) {
				disconnect();
			} else {
				MwnpMessage response = new MwnpMessage(new Integer[]{netId, 0}, cmd);
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
			MwnpMessage disconnect = new MwnpMessage(new Integer[]{netId, 0}, "MWNL2_DISCONNECT", null);
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
