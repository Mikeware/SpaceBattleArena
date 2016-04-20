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
 * @since 0.1
 * @version 1.1
 */
public class TextClient implements Client {
	private PrintStream logStream;
	private final boolean LOGGING = true;
	
	private int netId;
	private int shipId = -1;
	private MwnpListener listener;
	private MwnpMessenger messenger;
//	private String shipSuffix = "";
	
	private Spaceship<?> ship;	
	private Environment<?> env;
	
	private boolean disconnected = false;
	
	public TextClient(Spaceship<?> ship) {
		try {
			logStream = new PrintStream("client.log");
		} catch (FileNotFoundException ex) {
			System.err.println("Could not write to 'client.log' file.");
		}
		this.ship = ship;
	}
	
	public static void main(String[] args) {
		if (args == null || args.length < 2)
		{		
			System.err.println("Invalid parameters. Require IP Address and Class Name.");
			return;
		}
		
		try {
			run(args[0], (Spaceship<?>)Class.forName(args[1]).getConstructor().newInstance(), args.length > 2 ? Integer.parseInt(args[2]) : 2012);
		} catch (InvocationTargetException ex) {
			System.err.println("Exception constructing ship: " + ex.getMessage());
			ex.printStackTrace();
			return;
		} catch (IllegalAccessException ex) {
			System.err.println("Exception constructing ship: " + ex.getMessage());
			ex.printStackTrace();
			return;
		} catch (InstantiationException ex) {
			System.err.println("Exception constructing ship: " + ex.getMessage());
			ex.printStackTrace();
			return;
		} catch (NoSuchMethodException ex) {
			System.err.println("Exception constructing ship: " + ex.getMessage());
			ex.printStackTrace();
			return;
		} catch (ClassNotFoundException ex) {
			System.err.println("Cannot find ship class: " + ex.getMessage());
			ex.printStackTrace();
			return;
		} catch (ClassCastException ex) {
			System.err.println("Specified ship type does not implement Spaceship: " + ex.getMessage());
			ex.printStackTrace();
			return;
		}
	}
	
	public static void run(String ipAddress, Spaceship<?> ship) {
		run(ipAddress, ship, 2012);
	}
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void run(String ipAddress, Spaceship<?> ship, int socketNum) {

		System.out.println("Loading Ship " + ship.getClass().getSimpleName());
		TextClient client = new TextClient(ship);
		try {
			// Add disconnect hook
			Runtime.getRuntime().addShutdownHook(new ShutdownHook(client));

			// Connect to server
			System.out.println("Connecting to " + ipAddress);
			client.logMessage("Connecting to server...");
			Socket server = new Socket(ipAddress, socketNum);
			
			// Start listening for messages
			client.logMessage("Starting listener...");
			client.listener = new MwnpListener(client, server, "Listener Thead");
			client.listener.start();
			
			// Start sending messages
			client.logMessage("Starting messenger...");
			client.messenger = new MwnpMessenger(client, server, "Messenger Thread");
			client.messenger.start();
	
//			if (args.length > 3) {
//				System.out.println("Adding suffix " + args[3]);
//				client.shipSuffix = args[3];
//			}
			
			// Wait for termination command
			System.out.println("Type QUIT to disconnect from server and end program");
			BufferedReader kb = new BufferedReader(new InputStreamReader(System.in));
			while (!client.disconnected) {
				if (kb.ready()) {
					String input = kb.readLine();
					if (input.equalsIgnoreCase("quit")) {
						break;
					}
				}
			}
			kb.close();
		} catch (IOException ex) {
			System.err.println("Server connection failed.");
			System.err.println(ex.getMessage());
			ex.printStackTrace();
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
						
			// TODO: Some games may return extra data in the map, we should figure out how we want to expose this in the client
			RegistrationData data = ship.registerShip(numImages, width, height);
			data = new RegistrationData(data.getName(), data.getColor(), data.getImage());
			
			MwnpMessage response = new MwnpMessage(new Integer[]{netId, 0}, data);
			messenger.sendMessage(response);
		} else if (msg.getCommand().equals("ENV")) {
			env = (Environment<?>)msg.getData();

			// check for death
			int currShipId = env.getShipStatus().getId();
			if (shipId == -1) {
				shipId = currShipId;
			}
			
			if (shipId != currShipId) {
				// new id means ship has died; inform ship
				ship.shipDestroyed(((BasicGameInfo)env.getGameInfo()).getLastDestroyedBy());
				shipId = currShipId;
			}
			
			ShipCommand cmd = null;
			try {
				// Need to invoke through reflection as compiler doesn't know what type of Environment is here
				cmd = (ShipCommand)ship.getClass().getMethod("getNextCommand", Environment.class).invoke(ship, env);
			} catch (InvocationTargetException | NoSuchMethodException
					| SecurityException ex) {
				System.err.println("Error Invoking getNextCommand:");
				System.err.println(ex.getMessage());
				ex.printStackTrace(System.err);
				disconnect();
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
		if (!disconnected) {
			System.out.println("Attempting to disconnect...");
			
			logMessage("Sending disconnect message...");
			MwnpMessage disconnect = new MwnpMessage(new Integer[]{netId, 0}, "MWNL2_DISCONNECT", null);
			messenger.sendMessage(disconnect);
			logMessage("Ending listener...");
			listener.end();
			logMessage("Ending messenger...");
			messenger.end();
			
			disconnected = true;
			System.out.println("Disconnect complete.");
			
			BasicGameInfo gameInfo = (BasicGameInfo)(env.getGameInfo());
			System.out.println("\n**GAME STATISTICS**");
			System.out.printf("   Last round score: %f\n", gameInfo.getScore());
			System.out.printf("   Best round score: %f\n", gameInfo.getBestScore());
			System.out.printf("   Game high score: %f\n", gameInfo.getBestScore());
			System.out.printf("   Number of times destroyed: %d\n", gameInfo.getNumDeaths());
		}		
	}
	
	public boolean isDisconnected(){
		return this.disconnected;
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
