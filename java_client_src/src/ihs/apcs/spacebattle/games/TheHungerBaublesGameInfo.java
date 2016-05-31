package ihs.apcs.spacebattle.games;

import ihs.apcs.spacebattle.BasicGameInfo;
import ihs.apcs.spacebattle.ObjectStatus;
import ihs.apcs.spacebattle.Point;

import java.util.*;

/**
 * The Hunger Baubles are a game where you must hunt for the best collection of baubles.
 * 
 * Baubles have varying values and weights, and your ship can only carry so many.  You must use the Collect and Eject commands effectively in order
 * to pick and choose your baubles.
 * 
 * <p>
 * Your cargo hold has a maximum weight capacity of 25.
 * <p>
 * Blue Bauble are worth 1 point.<p>
 * Golden Baubles are worth 3 points.<p>
 * Red Baubles are worth 5 points.
 * <p>
 * If your ship is destroyed, the Baubles it was carrying will be dropped.
 * 
 * @author Michael A. Hawker
 *
 * @since 1.2
 * @version 1.2
 */
public class TheHungerBaublesGameInfo extends BasicGameInfo {
	private ArrayList<ObjectStatus> BAUBLES;
	
	/**
	 * Gets a list of the baubles in your cargo hold.
	 * Will be {@link ihs.apcs.spacebattle.ObjectStatus} classes with Mass, Value, and ID filled in.
	 * @return the set of baubles carried by the ship
	 */
	public List<ObjectStatus> getBaublesInCargo() {
		return BAUBLES;
	}
	
	/**
	 * Gets the number of baubles currently carried by your ship.
	 * @return the number of baubles carried by your ship
	 */
	public int getNumBaublesCarried() { return BAUBLES.size(); }
	
	/**
	 * Gets the value of the baubles being carried by your ship. 
	 * @return the value of the baubles carried by your ship
	 */
	public int getBaublesCarriedValue() {
		int value = 0;
		for (ObjectStatus obj : BAUBLES)
		{
			value += obj.getValue();
		}
		return value; 
	}
	
	/**
	 * Gets the total weight of the baubles being carried by your ship.
	 * @return weight of baubles carried
	 */
	public int getBaublesCarriedWeight() {
		int weight = 0;
		for (ObjectStatus obj : BAUBLES)
		{
			weight += obj.getMass();
		}
		return weight; 
	}
	
	@Override
	public String toString() {
		return String.format("{Target: %s; Score: %f; Deaths: %d; High Score: %f}", getObjectiveLocation(), getScore(), getNumDeaths(), getHighScore());
	}
}
