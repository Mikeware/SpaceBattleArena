package ihs.apcs.spacebattle;

import java.lang.reflect.Field;
import java.util.*;

/**
 * A class to represent the state of the world at the time a command is requested.
 * An Environment is passed to the {@link ihs.apcs.spacebattle.Spaceship#getNextCommand(Environment) } 
 * method of the {@link ihs.apcs.spacebattle.Spaceship} class to inform the ship of 
 * the current state of the world.
 * @author Brett Wortzman
 *
 */
public class Environment {
	private String[] MESSAGES;
	private int RADARLEVEL;
	private RadarResults RADARDATA;
	private ObjectStatus SHIPDATA;
	private GameInfo GAMEDATA;
		
	/**
	 * Gets a list of messages currently received.
	 * @return a list of messages
	 */
	public String[] getMessages() { return MESSAGES; }
	
	/**
	 * Gets the level of the last radar sweep.
	 * @return the level of radar sweep performed on the last command
	 */
	public int getRadarLevel() { return RADARLEVEL; }
	
	/**
	 * Gets the results of the most recent radar sweep.
	 * @return results of the radar sweep performed with the last command,
	 *   or null if the last command was not a radar sweep 
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
	public GameInfo getGameInfo() { return GAMEDATA; }
	
	
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
	public boolean equals(Environment other) {
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
