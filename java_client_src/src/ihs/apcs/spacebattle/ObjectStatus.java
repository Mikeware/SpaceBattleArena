/**
 * 
 */
package ihs.apcs.spacebattle;

import java.lang.reflect.Field;
import java.util.Arrays;

import ihs.apcs.spacebattle.util.StringMap;

/**
 * A class to represent the status of a ship or other object.  This class is used both to
 *   represent the current status of your ship in the {@link ihs.apcs.spacebattle.Environment }
 *   passed to {@link ihs.apcs.spacebattle.Spaceship#getNextCommand(Environment) }
 *   and the status of other objects found by a level 5 (fully-detailed) radar sweep.
 * @author Brett Wortzman
 *
 * @version 2.0
 * @since 1.0
 */
public class ObjectStatus {
	// Fields
	private int ID;
	private String TYPE;
	private double TIMEALIVE;

	private double[] POSITION;
	private double SPEED;
	private double MAXSPEED;
	private double DIRECTION;
	private int MASS;
	
	private double CURHEALTH;
	private double MAXHEALTH;
	private double CURENERGY;
	private double MAXENERGY;
	private double ENERGYRECHARGERATE;

	private double ROTATION; // Ship Only
	private double ROTATIONSPEED; // Ship Only
	private double CURSHIELD; // Ship Only
	private double MAXSHIELD; // Ship Only
	private int RADARRANGE; // Ship Only	
	
	// Game Specific
	private double VALUE; // Bubble, Bauble or Ship Only
	private int NUMSTORED; // Ship Only - Number of Baubles Carried
	private double HITRADIUS; // Bubble Only
	
	private int GRAVITY; // Planet/BlackHole Only
	private int GRAVITYFIELDLENGTH; // Planet/BlackHole Only	
	
	private int OWNERID; // Torpedo/HomeBase Only
	
	private String NAME; // If Turned on in Server Config
	
	// Getter methods
	/**
	 * Gets the object's Unique ID. 
	 * 
	 * Note: Ship IDs will change when they are destroyed.
	 * @return
	 */
	public int getId() { return ID; }
	/**
	 * String representation of the Type of Object.
	 * 
	 * Could be Ship, Planet, BlackHole, Asteroid, Torpedo,
	 * Bauble, Bubble, or HomeBase.
	 * 
	 * @return
	 */
	public String getType() { return TYPE; }
	/**
	 * Gets the amount of time this object has lived in seconds.
	 * @return
	 */
	public double getTimeAlive() { return TIMEALIVE; }

	/**
	 * Gets the position of this object.
	 * @return
	 */
	public Point getPosition() { return POSITION == null ? null : new Point(POSITION); }
	/**
	 * Gets this object's current speed.
	 * 
	 * Combine with its direction to get the Velocity Vector.
	 * @return
	 */
	public double getSpeed() { return SPEED; }
	/**
	 * Gets the maximum speed this object can travel.
	 * @return
	 */
	public double getMaxSpeed() { return MAXSPEED; }
	/**
	 * Get the actual direction of Movement of this object.  This may not equal its Orientation.
	 * @return
	 */
	public double getMovementDirection() { return DIRECTION; }
	/**
	 * Gets this object's mass.
	 * @return
	 */
	public int getMass() { return MASS; }
	
	/**
	 * Gets the current Health of this object.
	 * 
	 * When an object has zero or less health, it is destroyed.
	 * @return
	 */
	public double getHealth() { return CURHEALTH; }
	/**
	 * Gets the maximum amount of health this object could have. (100 for Ships)
	 * @return
	 */
	public double getMaxHealth() { return MAXHEALTH; }
	/**
	 * Gets the current amount of energy this object has.
	 * @return
	 */
	public double getEnergy() { return CURENERGY; }
	/**
	 * Gets the maximum amount of energy this object could store. (100 for Ships)
	 * @return
	 */
	public double getMaxEnergy() { return MAXENERGY; }
	/**
	 * Gets the amount of energy this object restores per second.
	 * @return
	 */
	public double getRechargeRate() { return ENERGYRECHARGERATE; }
	
	// Ship Only
	/**
	 * Gets the current Orientation of a Ship.
	 * @return
	 */
	public double getOrientation() { return ROTATION; }
	/**
	 * Gets the number of degrees this Ship can turn in a second (default is 120).
	 * @return
	 */
	public double getRotationSpeed() { return ROTATIONSPEED; }
	/**
	 * Gets the current Shield strength of a Ship.
	 * @return
	 */
	public double getShieldLevel() { return CURSHIELD; }
	/**
	 * Gets the maximum amount of Shields the Ship object could have. (default is 100)
	 * @return
	 */
	public double getMaxShield() { return MAXSHIELD; }
	/**
	 * Gets the radius from a Ship object that its radar can detect objects. 
	 * @return
	 */
	public int getRadarRange() { return RADARRANGE; }
	
	/**
	 * Gets the point value worth of a Bubble, Bauble, or Ship in a Game.
	 * @return
	 */
	public double getValue() { return VALUE; }
	
	/**
	 * Gets the number of cargo items carried by a Ship in a Game. 
	 * @return
	 */
	public int getNumberStored() { return NUMSTORED; }
	
	/**
	 * Gets the radius of the object needed for collision detection. This tells you an object's size.
	 * @return
	 */
	public double getHitRadius() { return HITRADIUS; }
	
	/**
	 * Gets the strength of the gravity of a Planet or BlackHole. A higher number represents a stronger pull.
	 * @return
	 */
	public int getGravityStrength() { return GRAVITY; }
	/**
	 * Gets the radius around a Planet or BlackHole that will cause a gravity effect.
	 * @return
	 */
	public int getGravityFieldLength() { return GRAVITYFIELDLENGTH; }
	
	/**
	 * Gets the ID of the Owner of this object.  This could be who fired a Torpedo or who owns a HomeBase.
	 * @return
	 */
	public int getOwnerId() { return OWNERID; }
	
	/**
	 * Gets the name of this object. (may be turned off on the server)
	 * @return
	 */
	public String getName() { return NAME; }
	
	public String toString() {
		try {
			StringMap<Object> map = new StringMap<Object>();
			for (Field f : getClass().getDeclaredFields()) {
				f.setAccessible(true);
				Object val = f.get(this);
				if (val != null) {
					if (f.getName().equals("POSITION")) {
						map.put(f.getName(), Arrays.toString((double[])val));
					} else {
						map.put(f.getName(), val);
					}
				}
			}
		return map.toString();
		} catch (Exception e) {
			return "";
		}
	}
	
	public boolean equals(ObjectStatus other) {
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
