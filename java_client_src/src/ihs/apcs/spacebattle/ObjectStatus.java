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
	private double ROTATION; // Ship Only
	private double ROTATIONSPEED; // Ship Only

	private double SCORE; // Ship Only
	private double CURHEALTH;
	private double MAXHEALTH;
	private double CURENERGY;
	private double MAXENERGY;
	private double ENERGYRECHARGERATE;
	private double CURSHIELD; // Ship Only
	private double MAXSHIELD; // Ship Only

	private int RADARRANGE; // Ship Only
	private int MASS;
	private double HITRADIUS; // Bubble Only
	private int GRAVITY; // Planet/BlackHole Only
	private int GRAVITYFIELDLENGTH; // Planet/BlackHole Only
	
	private double BUBBLEPOINTS; // Bubble Only
	private int OWNERID; // Torpedo/HomeBase Only
	private String NAME;
	
	// Getter methods
	public int getId() { return ID; }
	public String getType() { return TYPE; }
	public double getTimeAlive() { return TIMEALIVE; }

	public Point getPosition() { return POSITION == null ? null : new Point(POSITION); }
	public double getSpeed() { return SPEED; }
	public double getMaxSpeed() { return MAXSPEED; }
	public double getMovementDirection() { return DIRECTION; }
	public double getOrientation() { return ROTATION; }
	public double getRotationSpeed() { return ROTATIONSPEED; }

	public double getScore() { return SCORE; }
	public double getHealth() { return CURHEALTH; }
	public double getMaxHealth() { return MAXHEALTH; }
	public double getEnergy() { return CURENERGY; }
	public double getMaxEnergy() { return MAXENERGY; }
	public double getRechargeRate() { return ENERGYRECHARGERATE; }
	public double getShieldLevel() { return CURSHIELD; }
	public double getMaxShield() { return MAXSHIELD; }

	public int getRadarRange() { return RADARRANGE; }
	public int getMass() { return MASS; }
	public double getHitRadius() { return HITRADIUS; }
	public int getGravityStrength() { return GRAVITY; }
	public int getGravityFieldLength() { return GRAVITYFIELDLENGTH; }
	
	public double getBubblePoints() { return BUBBLEPOINTS; }
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
