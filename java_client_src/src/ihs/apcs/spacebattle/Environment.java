package ihs.apcs.spacebattle;

import java.lang.reflect.Field;
import java.util.*;

/**
 * A class to represent the state of the world at the time a command is requested.
 * An Environment is passed to the {@link ihs.apcs.spacebattle.Spaceship#getNextCommand(Environment) } 
 * method of the {@link ihs.apcs.spacebattle.Spaceship} class to inform the ship of 
 * the current state of your ship and the world.
 * The Environment may contain additional information based on performing other commands like {@link ihs.apcs.spacebattle.commands.RadarCommand }.
 * @author Brett Wortzman
 * @version 2.0
 * @since 1.0
 * 
 * @param <T> specify the corresponding Game class to that being played on the server.  Corresponds to the same class used by the {@link ihs.apcs.spacebattle.Spaceship} interface. 
 */
public class Environment<T> {
	protected String[] MESSAGES;
	protected int RADARLEVEL;
	protected RadarResults RADARDATA;
	protected ObjectStatus SHIPDATA;
	protected T GAMEDATA;
		
	/**
	 * Gets a list of messages currently received. [Not Used]
	 * @return a list of messages
	 */
	public String[] getMessages() { return MESSAGES; }
	
	/**
	 * Gets the level of the last radar sweep, if the last command issued was a {@link ihs.apcs.spacebattle.commands.RadarCommand }.
	 * @return the level of radar sweep performed by the {@link ihs.apcs.spacebattle.commands.RadarCommand }.
	 */
	public int getRadarLevel() { return RADARLEVEL; }
	
	/**
	 * Gets the results of the most recent radar sweep, if and only if the last command issued was a {@link ihs.apcs.spacebattle.commands.RadarCommand }.
	 * @return results of the radar sweep performed with the last {@link ihs.apcs.spacebattle.commands.RadarCommand },
	 *   or null if the last command issued was not a radar sweep 
	 */
	public RadarResults getRadar() { return RADARDATA; }
	
	/**
	 * Gets the status of your ship.
	 * @return the status of your ship
	 */
	public ObjectStatus getShipStatus() { return SHIPDATA; }
	
	/**
	 * Gets information concerning the current game objective.
	 * @return information about the current game, or null if no game
	 *   is in progress
	 */
	public T getGameInfo() { return GAMEDATA; }
	
	
	public String toString() {
		StringBuilder build = new StringBuilder();
		build.append("MESSAGES: ");
		build.append(Arrays.toString(MESSAGES));
		
		build.append(", GAMEINFO: ");
		build.append(getGameInfo());

		build.append(", RADARLEVEL: ");
		build.append(getRadarLevel());
		
		build.append(", RADARDATA: ");
		build.append(getRadar());
		
		build.append(", SHIPDATA: ");
		build.append(getShipStatus());
		
		
		return build.toString();
	}
	
	/**
	 * Determines if this Environment is the same as another one.  Two 
	 *   Environments are equal if they contain all the same data.
	 * @param other the Environment to compare to
	 * @return true if the Environments are equal, false otherwise
	 */
	public boolean equals(Environment<T> other) {
		try {
			for (Field f : getClass().getDeclaredFields()) {
				f.setAccessible(true);
				Object thisVal = f.get(this);
				Object otherVal = f.get(other);
				if (!thisVal.equals(otherVal))
					return false;
			}
			return true;
		} catch (Exception ex) {
			return false;
		}
	}

}
