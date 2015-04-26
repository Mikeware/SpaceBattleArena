package ihs.apcs.spacebattle;

import ihs.apcs.spacebattle.commands.ShipCommand;

/**
 * Represents a ship in the Space Battle world.
 * <p>
 * Spaceship's are autonomous and issue commands through callbacks 
 * to the server using this class's methods.  The flow operations is as follows:
 * <ol>
 * 	<li>Client connects to the server</li>
 *  <li>Server requests registration</li>
 *  <li>Client calls {@link #registerShip(int, int, int)} to get registration 
 *  	information and forwards registration to the server</li>
 *  <li>Server responds by sending back an {@link Environment} and waiting for 
 *  	a command</li>
 *  <li>Client calls {@link #getNextCommand(Environment)} and sends the returned 
 *  	command back to the server</li>
 *  <li>Repeat 4-5</li>
 * </ol>  
 * 
 * @author Brett Wortzman
 *
 */
public interface Spaceship {
	/**
	 * Registers a ship with the server so it can begin issuing commands.
	 * @param numImages the number of images available for the ship's 
	 * 			appearance on the server
	 * @param worldWidth the width of the current world in pixels
	 * @param worldHeight the height of the current world in pixels
	 * @return the necessary registration information for the server
	 */
	public RegistrationData registerShip(int numImages, int worldWidth, int worldHeight);
	
	/**
	 * Issues a command to be executed by this ship on the server.
	 * <p>
	 * Commands are executed one at a time, except for non-blocking commands.
	 * Commands cannot be issued except when requested by the server.  The
	 * server will process each command, then send the new environment
	 * (representing the result of the issued command and any actions taken by
	 * other entities in the game world) back to the ship and request a new 
	 * command.
	 * @param env the current environment provided by the server
	 * @return a command to be executed by the ship
	 */
	public ShipCommand getNextCommand(Environment env);
	
	/**
	 * Notifies a ship that it has been destroyed and respawned.  Ships can use this to track their deaths.
	 */
	public void shipDestroyed();
	
	
	//public void processError(ErrorData error);
}
