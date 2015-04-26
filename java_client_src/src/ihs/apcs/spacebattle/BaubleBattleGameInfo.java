package ihs.apcs.spacebattle;

import java.util.*;

/**
 * Represents the pertinent information to play the Bauble Hunt game.
 * @author Brett Wortzman
 *
 */
public class BaubleBattleGameInfo {
	private double[] POSITION;
	private double[][] BAUBLES;
	private int SCORE;
	private int COLLECTED;
	private int HIGHSCORE;
	private int DEATHS;
	private int STORED;
	private int STOREDVALUE;
	
	/**
	 * Gets the position of your home base.
	 * @return the position of your home base
	 */
	public Point getHomeBasePosition() { return new Point(POSITION); }
	
	/**
	 * Gets a list of positions where there are baubles.  Not all
	 *   bauble positions are returned, but each position in the list
	 *   has a bauble (unless it has been collected already).
	 * @return a list of bauble positions
	 */
	public List<Point> getBaublePositions() {
		List<Point> result = new ArrayList<Point>();
		for (double[] pos : BAUBLES) {
			result.add(new Point(pos));
		}
		return result;
	}
	
	/**
	 * Gets your current score.
	 * @return your current score
	 */
	public int getScore() { return SCORE; }
	
	/**
	 * Gets the number of baubles collected and returned to your base.
	 * @return the number of baubles return to base
	 */
	public int getNumCollected() { return COLLECTED; }
	
	/**
	 * Gets the number of baubles currently carried by your ship (maximum of 5).
	 * @return the number of baubles carried by your ship
	 */
	public int getNumBaublesCarried() { return STORED; }
	
	/**
	 * Gets the value of the baubles being carried by your ship (maximum of 25). 
	 * @return the value of the baubles carried by your ship
	 */
	public int getBaublesCarriedValue() { return STOREDVALUE; }
	
	/**
	 * Gets the current game leader's score.
	 * @return the current game leader's score
	 */
	public int getHighScore() { return HIGHSCORE; }
	
	/**
	 * Gets the number of times you have died in this game.
	 * @return your number of deaths for this game 
	 */
	public int getNumDeaths() { return DEATHS; }

	@Override
	public String toString() {
		return String.format("{Target: %s; Score: %d; Deaths: %d; High Score: %d}", getHomeBasePosition(), getScore(), getNumDeaths(), getHighScore());
	}
}
