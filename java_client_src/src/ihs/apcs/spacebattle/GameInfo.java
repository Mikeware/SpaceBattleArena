package ihs.apcs.spacebattle;

import java.util.*;

/**
 * Represents the pertinent information to play the "King of the Bubble" game.
 * @author Brett Wortzman
 *
 */
public class GameInfo {
	private double[][] BUBBLES;
	private double SCORE;
	private double HIGHSCORE;
	private int DEATHS;
	
	private List<Point> bubblePositions;
	
	/**
	 * Gets your current score.
	 * @return your current score
	 */
	public double getScore() { return SCORE; }
	
	/**
	 * Gets the current game leader's score.
	 * @return the current game leader's score
	 */
	public double getHighScore() { return HIGHSCORE; }

	/**
	 * Gets the number of times you have died in this game.
	 * @return your number of deaths for this game.
	 */
	public int getNumDeaths() { return DEATHS; }
	
	/**
	 * Gets the positions of all current bubbles in the world.  Note that it is only guaranteed
	 *   that a bubble existed at this location when the {@link Environment} was created.  The 
	 *   bubble may have dissipated before you get there.
	 * @return a list of all bubble positions
	 */
	public List<Point> getBubblePositions() {
		if (bubblePositions == null) {
			bubblePositions = new ArrayList<Point>();
		}
		if  (BUBBLES != null) {
			for (double[] pos : BUBBLES) {
				bubblePositions.add(new Point(pos));
			}
		}
		return bubblePositions;
	}
	
	@Override
	public String toString() {
		return String.format("{Score: %f; Deaths: %d; High Score: %f; Num. Bubbles: %d}", getScore(), getNumDeaths(), getHighScore(), getBubblePositions() == null ? 0 : getBubblePositions().size());
	}
}
