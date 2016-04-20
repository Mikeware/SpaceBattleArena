package ihs.apcs.spacebattle.commands;

import java.util.*;
import java.lang.reflect.*;

import ihs.apcs.spacebattle.util.*;

/**
 * @author Brett Wortzman
 *
 * @since 0.1
 * @version 1.1
 */
public abstract class ShipCommand {
	protected abstract String getName();
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command
	 */
	public static int getInitialEnergyCost() { return 0; }
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing
	 */
	public static int getOngoingEnergyCost() { return 0; }
	
	/**
	 * Returns true if the Command will stop other commands from processing. (default true)
	 * 
	 * @since 1.1
	 * @return true if the command blocks (default).
	 */
	public static boolean isBlocking() { return true; }
	
	/**
	 * Returns true if the Command executes as soon as it is processed in the queue and does not delay for any period of time. (default false)
	 * 
	 * All commands which execute immediately are blocking commands; however, since they don't delay, there is not much impact to consider besides energy costs.
	 * @since 1.1
	 * @return false by default
	 */
	public static boolean executesImmediately() { return false; }
	
	public ArrayList<Object> getMessage() throws IllegalArgumentException, IllegalAccessException {
		ArrayList<Object> list = new ArrayList<Object>();
		list.add(getName());
		if (getArgs() != null && getArgs().size() > 0)
			list.add(getArgs());
		return list;
	}
	
	protected StringMap<Object> getArgs() throws IllegalArgumentException, IllegalAccessException {
		StringMap<Object> map = new StringMap<Object>();
		for (Field f : getClass().getDeclaredFields()) {
			f.setAccessible(true);
			Object val = f.get(this);
			if (val != null)
				map.put(f.getName(), val);
		}
		return map;
	}
	
	public boolean equals(ShipCommand other) {
		// if the commands aren't of the same type, they're not equal
//		if (!(this.getClass().isInstance(other)))
//			return false;
		
		// commands are equal if all of their fields are equal
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

	public String toString() {
		try {
			return String.format("%s[%s]", getName(), getArgs());
		} catch (Exception ex) {
			return getName();
		}
	}
}
