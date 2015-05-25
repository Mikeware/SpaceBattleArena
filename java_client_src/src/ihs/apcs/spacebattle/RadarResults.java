package ihs.apcs.spacebattle;

import java.util.*;

/**
 * Represents the results of a radar sweep.
 * <p>
 * Each radar sweep will return a collection of {@link ihs.apcs.spacebattle.ObjectStatus} 
 *   objects representing the objects in range of the radar sweep.  If a level 
 *   1, 2, or 4 sweep was performed, these {@link ihs.apcs.spacebattle.ObjectStatus}es 
 *   will not be fully populated.  Attempting to access data that was not determined
 *   by the radar sweep will result in a zero-equivalent value.
 * @author Brett Wortzman
 * @see ihs.apcs.spacebattle.commands.RadarCommand
 */
public class RadarResults extends ArrayList<ObjectStatus> {
	private static final long serialVersionUID = -5552710352589416751L;

	/**
	 * Gets the number of objects detected by this radar sweep.
	 * <p>
	 * <i>Note: for a level 3 sweep, this will be either 0 or 1.</i>
	 * @return the number of objects detected by the radar sweep
	 */
	public int getNumObjects() {
		return this.size(); 
	}
	
	/**
	 * Gets the details read by this radar sweep for a particular object whose 
	 *   ID is previously known. 
	 * @param id the ID of the object to lookup
	 * @return the radar details for the given object, or null if the object
	 *   was not detected in this sweep
	 */
	public ObjectStatus getById(int id) {
		for (ObjectStatus s : this) {
			if (s.getId() == id) 
				return s;
		}
		return null;
	}
	
	/**
	 * Gets the details read by this radar sweep for a particular object whose 
	 *   location is previously known. 
	 * @param pos the position of the object to lookup
	 * @return the radar details for the given object, or null if the object
	 *   was not detected in this sweep
	 */
	public ObjectStatus getByPosition(Point pos) {
		for (ObjectStatus s: this) {
			if (s.getPosition() != null && s.getPosition().equals(pos))
				return s;
		}
		return null;
	}
	
	/**
	 * Gets the details read by this radar sweep for all objects of the given
	 *   type.  Case-insensitive comparison is used for type names.
	 *
	 * <p>Could be Ship, Planet, BlackHole, Asteroid, Torpedo, Nebula,
	 * Bauble, Bubble, or HomeBase.
	 *
	 * @param type the type of object for which to return results
	 * @return a list of radar details for all objects of the given type (may be empty)
	 */
	public List<ObjectStatus> getByType(String type) {
		List<ObjectStatus> list = new ArrayList<ObjectStatus>();
		for (ObjectStatus s : this) {
			if (s.getType() != null && s.getType().equalsIgnoreCase(type)) {
				list.add(s);
			}
		}
		return list;
	}
}
