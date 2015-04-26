/**
 * 
 */
package ihs.apcs.spacebattle;

import java.lang.reflect.Field;
import java.util.Arrays;

import ihs.apcs.spacebattle.util.StringMap;

/**
 * A class to represent the status of a ship.  This class is used both to
 *   represent the current status of your ship in the {@link ihs.apcs.spacebattle.Environment }
 *   passed to {@link ihs.apcs.spacebattle.Spaceship#getNextCommand(Environment) }
 *   and the status of other ships found by a level 5 (fully-detailed) radar sweep.
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
	public double getTimeAlive() { return TIMEALIVE; }

	public Point getPosition() { return POSITION == null ? null : new Point(POSITION); }
	public double getSpeed() { return SPEED; }
	public double getMaxSpeed() { return MAXSPEED; }
	public double getMovementDirection() { return DIRECTION; }
	public int getMass() { return MASS; }
	
	public double getHealth() { return CURHEALTH; }
	public double getMaxHealth() { return MAXHEALTH; }
	public double getEnergy() { return CURENERGY; }
	public double getMaxEnergy() { return MAXENERGY; }
	public double getRechargeRate() { return ENERGYRECHARGERATE; }
	
	// Ship Only
	public double getOrientation() { return ROTATION; }
	public double getRotationSpeed() { return ROTATIONSPEED; }
	public double getShieldLevel() { return CURSHIELD; }
	public double getMaxShield() { return MAXSHIELD; }
	public int getRadarRange() { return RADARRANGE; }
	
	/**
	 * Gets the point value worth of a Bubble, Bauble, or Ship.
	 * @return
	 */
	public double getValue() { return VALUE; }
	/**
	 * Gets the number of cargo items carried by a Ship. 
	 * @return
	 */
	public int getNumberStored() { return NUMSTORED; }
	
	public double getHitRadius() { return HITRADIUS; }
	
	public int getGravityStrength() { return GRAVITY; }
	public int getGravityFieldLength() { return GRAVITYFIELDLENGTH; }
	
	public int getOwnerId() { return OWNERID; }
	
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
