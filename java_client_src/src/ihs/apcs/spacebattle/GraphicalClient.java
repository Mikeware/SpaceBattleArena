/**
 * Space Battle Arena is a Programming Game.
 *
 * Copyright (C) 2012-2016 Michael A. Hawker and Brett Wortzman
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

import ihs.apcs.spacebattle.commands.IdleCommand;
import ihs.apcs.spacebattle.commands.ShipCommand;
import ihs.apcs.spacebattle.networking.*;
import ihs.apcs.spacebattle.util.StringStringMap;

import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.net.Socket;
import java.text.DateFormat;
import java.util.Calendar;
import java.util.Scanner;

import javax.swing.*;

public class GraphicalClient implements Runnable, Client {
	private final boolean LOGGING = true;
	
	private int netId;
	private MwnpListener listener;
	private MwnpMessenger messenger;
	private String shipClassname;
	private Spaceship<?> ship;
	private Class<?> shipType;
	
	private String[] args;
	private JFrame frame;
	
	private boolean disconnected = false;
	
	public GraphicalClient(String[] args) throws FileNotFoundException {
		this.args = args;
	}

	@Override
	public void run() {
		frame = new JFrame("Robots......in SPACE!!!");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
		try {
			// Connect to server
			this.logMessage("Connecting to server...");
			Socket server = new Socket(args[0], 2012);
			
			// Add disconnect hook
			Runtime.getRuntime().addShutdownHook(new ShutdownHook(this));

			// Start listening for messages
			this.logMessage("Starting listener...");
			this.listener = new MwnpListener(this, server, "Listener Thead");
			this.listener.start();
			
			// Start sending messages
			this.logMessage("Starting messenger...");
			this.messenger = new MwnpMessenger(this, server, "Messenger Thread");
			this.messenger.start();
			
			// Create ship
			this.shipClassname = args[1];
			Class<?> shipType = Class.forName(this.shipClassname);
			this.logMessage("Creating new " + shipType.getName());
			this.ship = (Spaceship<?>)shipType.getConstructor().newInstance();
			
			System.out.println("Type QUIT to disconnect from server and end program");
			Scanner kb = new Scanner(System.in);
			while (kb.hasNextLine() && !kb.nextLine().equalsIgnoreCase("QUIT"));
			kb.close();
		} catch (IOException ex) {
			System.err.println("Server connection failed.");
			System.err.println(ex.getMessage());
			System.err.println(ex.getStackTrace());
		} catch (ClassCastException ex) {
			System.err.println("Specified ship type does not implement Spaceship.");
			System.err.println(ex.getMessage());
		} catch (ClassNotFoundException ex) {
			System.err.println("Specified ship type not found.");
			System.err.println(ex.getMessage());
		} catch (Exception ex) {
			System.err.println(ex.getMessage());
			ex.printStackTrace();
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
			
			MwnpMessage response = new MwnpMessage(new Integer[]{netId, 0}, data);
			messenger.sendMessage(response);
		} else if (msg.getCommand().equals("ENV")) {
			Environment<?> env = (Environment<?>)msg.getData();
			
			ShipCommand cmd = null;
			try {
				cmd = (ShipCommand)shipType.getMethod("getNextCommand",  Environment.class).invoke(ship,  env);
			} catch (InvocationTargetException | NoSuchMethodException
					| SecurityException ex) {
				System.err.println("Error Invoking getNextCommand:");
				System.err.println(ex.getMessage());
				ex.printStackTrace(System.err);
			}
			
			if (cmd == null) {
				cmd = new IdleCommand(0.1);
			} else {
				MwnpMessage response = new MwnpMessage(new Integer[]{netId, 0}, cmd);
				messenger.sendMessage(response);
			}
		} else if (msg.getCommand().equals("ERROR")) {
			System.out.println(msg.getData());
		}
	}
	
	public void disconnect() throws IOException {
		System.out.println("Attempting to disconnect...");
		if (!disconnected) {
			System.out.println("Sending disconnect message...");
			MwnpMessage disconnect = new MwnpMessage(new Integer[]{netId, 0}, "MWNL2_DISCONNECT", null);
			messenger.sendMessage(disconnect);
			System.out.println("Ending listener...");
			listener.end();
			System.out.println("Ending messenger...");
			messenger.end();
		}
		disconnected = true;
		System.out.println("Disconnect complete.");
	}
	
	public boolean isDisconnected(){
		return this.disconnected;
	}
	
	public void logMessage(String message) {
		if (LOGGING) {
			Calendar now = Calendar.getInstance();
			String msg = String.format("LOG: %s: %s\n", DateFormat.getDateTimeInstance().format(now.getTime()), message);
			
			frame.getContentPane().add(new JLabel(msg));
		}
	}
	
	public static void main(String[] args) throws InterruptedException, InvocationTargetException, FileNotFoundException {
		GraphicalClient client = new GraphicalClient(args);
		SwingUtilities.invokeLater(client);
	}

}
