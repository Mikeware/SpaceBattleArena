package ihs.apcs.spacebattle.games;

import ihs.apcs.spacebattle.BasicGameInfo;
import ihs.apcs.spacebattle.Point;

import java.util.*;

/**
 * "King of the Bubble" is a game where there are a number of 'Bubbles' in the world worth some amount of points.
 * <p>
 * By placing your ship within the Bubble, you will absorb its points.
 * <p>
 * When your ship is destroyed, you may drop a new Bubble in the world which represents some amount of the points you have (which are now lost).
 * <p>
 * Multiple ships within the same Bubble will drain it's points faster.  It is also possible to drain points from multiple Bubbles at the same time.
 * <p>
 * Bubbles will eventually start to shrink and disappear on their own.
 * 
 * @author Brett Wortzman
 *
 * @since 1.2
 * @version 2.0
 */
public class KingOfTheBubbleGameInfo  extends BasicGameInfo {
	private double[][] BUBBLES;
	
	private List<Point> bubblePositions;
		
	/**
	 * Gets the positions of all current bubbles in the world.  Note that it is only guaranteed
	 *   that a bubble existed at this location when the {@link ihs.apcs.spacebattle.Environment } was created.  The 
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
