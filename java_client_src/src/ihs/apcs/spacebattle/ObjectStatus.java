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
 * @since 0.1
 * @version 1.2
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
	private long MASS;
	
	private double CURHEALTH;
	private double MAXHEALTH;
	private double CURENERGY;
	private double MAXENERGY;
	private double ENERGYRECHARGERATE;

	private int ROTATION; // Ship,Nebula Only
	private int ROTATIONSPEED; // Ship Only
	private double CURSHIELD; // Ship Only
	private double MAXSHIELD; // Ship Only
	private int RADARRANGE; // Ship Only
	private int CMDLEN; // Ship Only
	private boolean INBODY; // Ship or Celestial Body Only;
	
	// Game Specific
	private double VALUE; // Bubble, Bauble or Ship Only
	private int NUMSTORED; // Ship Only - Number of Baubles Carried
	private double HITRADIUS; // Round Only
    private boolean SUCCESS; // Game boolean for success for this object
	
	private int PULL; // Planet/BlackHole/Nebula Only
	private int MAJOR; // Planet/BlackHole/Nebula Only
	private int MINOR; // Planet/BlackHole/Nebula Only
	
	private int OWNERID; // Torpedo/HomeBase Only
	
	private String NAME; // If Turned on in Server Config
	
	// Getter methods
	/**
	 * Gets the object's Unique ID. 
	 * 
	 * Note: Ship IDs will change when they are destroyed.
	 * @return a unique identifier for the object
	 */
	public int getId() { return ID; }
	/**
	 * String representation of the Type of Object.
	 * 
	 * Could be Ship, Planet, BlackHole, Star, Nebula, Asteroid, Dragon, Torpedo,
	 * Bauble, Bubble, or Outpost.
	 * 
	 * @return name of the object's type.
	 */
	public String getType() { return TYPE; }
	/**
	 * Gets the amount of time this object has lived in seconds.
	 * @return seconds alive.
	 */
	public double getTimeAlive() { return TIMEALIVE; }

	/**
	 * Gets the position of this object within the world (0, 0) is the upper-left and increases down and to the right.
	 *
	 * @return the x, y position in pixel coordinates as a {@link ihs.apcs.spacebattle.Point }.
	 */
	public Point getPosition() { return POSITION == null ? null : new Point(POSITION); }
	/**
	 * Gets this object's current speed.
	 * 
	 * Combine with its direction to get a Velocity Vector.
	 * @return current speed in pixels per second
	 */
	public double getSpeed() { return SPEED; }
	/**
	 * Gets the maximum speed this object can travel.
	 * @return upper-bound of obtainable speed
	 */
	public double getMaxSpeed() { return MAXSPEED; }
	/**
	 * Get the actual direction of travel for this object.  This may not equal its the direction it is facing (orientation) {@link #getOrientation() }
	 * @return angle in degrees
	 * 
	 * @version 1.2
	 */
	public double getMovementDirection() { return (DIRECTION + 360.0) % 360.0; }
	/**
	 * Gets this object's mass.
	 * @return mass value.
	 */
	public long getMass() { return MASS; }
	
	/**
	 * Gets the current Health of this object.
	 * 
	 * When an object has zero or less health, it is destroyed.
	 * @return health remaining.
	 */
	public double getHealth() { return CURHEALTH; }
	/**
	 * Gets the maximum amount of health this object could have. (100 for Ships)
	 * @return upper-bound of health value.
	 */
	public double getMaxHealth() { return MAXHEALTH; }
	/**
	 * Gets the current amount of energy this object has.
	 * @return energy remaining.
	 */
	public double getEnergy() { return CURENERGY; }
	/**
	 * Gets the maximum amount of energy this object could store. (100 for Ships)
	 * @return upper-bound of energy value.
	 */
	public double getMaxEnergy() { return MAXENERGY; }
	/**
	 * Gets the amount of energy this object restores per second.
	 * @return energy per second restored.
	 */
	public double getRechargeRate() { return ENERGYRECHARGERATE; }
	
	// Ship Only
	/**
	 * Gets the current Orientation of a Ship or Nebula.
	 * @return the orientation in degrees.
	 * 
	 * @version 1.2
	 */
	public int getOrientation() { return (ROTATION + 360) % 360; }
	
	/**
	 * Gets the number of degrees this Ship can turn in a second (default is 120).
	 * @return speed in degrees per second the ship can rotate.
	 * 
	 * @version 1.2
	 */
	public int getRotationSpeed() { return ROTATIONSPEED; }
	
	/**
	 * Gets the current Shield strength of a Ship.
	 * @return shields remaining.
	 */
	public double getShieldLevel() { return CURSHIELD; }
	
	/**
	 * Gets the maximum amount of Shields the Ship object could have. (default is 100)
	 * @return upper-bound of shield value.
	 */
	public double getMaxShield() { return MAXSHIELD; }
	
	/**
	 * Gets the radius from a Ship object that its radar can detect objects. 
	 * @return radar radius.
	 */
	public int getRadarRange() { return RADARRANGE; }
	
	/**
	 * Gets the number of commands your Ship is currently executing.
	 * @return number of commands being executed
	 */
	public int getCommandQueueLength() { return CMDLEN; }
	
	/**
	 * Is this object in a celestial object's body of effect?
	 * @return true if a ship is in a celestial body's main area of effect (could be false but in gravity well still {@link #getAxisMajorLength()}).
	 * A celestial body will return true if it contains an object like a ship.
     *
     * @since 1.1
	 */
	public boolean isInCelestialBody() { return INBODY; }
	
   /**
    * Was an object successfully scanned for a game? (Discovery Quest)
    * @return true if this object has a value of success for the current game.
    * i.e. Successfully scanned in Discovery Quest.
    *
    * @since 1.1
    */
   public boolean isSuccessful() { return SUCCESS; }
   
	/**
	 * Gets the point value worth of a Bubble, Bauble, or Ship in a Game.
	 * @return point value.
	 */
	public double getValue() { return VALUE; }
	
	/**
	 * Gets the number of cargo items carried by a Ship in a Game. 
	 * @return number of items/points
	 */
	public int getNumberStored() { return NUMSTORED; }
	
	/**
	 * Gets the radius of the object needed for collision detection. This tells you an object's radius.
	 * @return the radius of the object from its {@link ihs.apcs.spacebattle.ObjectStatus#getPosition() }
	 */
	public double getHitRadius() { return HITRADIUS; }
	
	/**
	 * Gets the strength of the gravity or drag of a Planet, BlackHole or Nebula. A higher number represents a stronger effect.
	 * @return pull value.
     * @since 1.0
	 */
	public int getPullStrength() { return PULL; }
	/**
	 * Gets the length of a Planet, BlackHole, or Nebula on its major axis.  For Planets and BlackHoles, the Major and Minor lengths will be the same.
	 * <p>
	 * For Planets and BlackHoles this length represents the size of the gravitational field around it.  The {@link #getPullStrength()} method will tell you how much it will effect your ship.
	 * <p>
	 * For Nebula this length is oriented in the Nebula's direction/rotation see {@link #getOrientation() } and represents its major radius.  If your ship is in the Nebula, it will slow down based on the {@link #getPullStrength()} amount.
	 * @return the elliptical radius along the parallel axis
     * @since 1.0
	 */
	public int getAxisMajorLength() { return MAJOR; }
	
	/**
	 * Gets the length from the center of a Nebula that is perpendicular to the direction/rotation of the Nebula.
	 * @return the elliptical radius along the perpendicular axis
     * @since 1.0
	 */
	public int getAxisMinorLength() { return MINOR; }
	
	/**
	 * Gets the ID of the Owner of this object.  This could be who fired a Torpedo or who owns an Outpost (Bauble Hunt).
	 * @return the owner id of this object (if any)
	 */
	public int getOwnerId() { return OWNERID; }
	
	/**
	 * Gets the name of a Ship object. (may be turned off on the server but see {@link #getType() })
	 * @return a name of a Ship
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
