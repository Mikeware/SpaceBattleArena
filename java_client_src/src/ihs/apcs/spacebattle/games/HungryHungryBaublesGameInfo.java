/**
 * 
 */
package ihs.apcs.spacebattle.games;

import ihs.apcs.spacebattle.BasicGameInfo;
import ihs.apcs.spacebattle.Point;

/**
 * Hungry Hungry Baubles is a game where you must collect Baubles within the world for points.
 * <p>
 * There are regular Baubles and 'Golden' Baubles.  
 * <p>
 * Regular Baubles are worth 1 point.<p>
 * Golden Baubles are worth 3 points.
 * <p>
 * You are assigned a specific Golden Bauble, if you collect it, it's worth an additional 2 points.  You will be then assigned another Golden Bauble to collect. 
 * 
 * @author Michael A. Hawker
 *
 * @since 2.0
 * @version 1.0
 */
public class HungryHungryBaublesGameInfo extends BasicGameInfo {
	private double[] POSITION;
	
	/**
	 * Gets the position of your assigned golden Bauble.
	 * @return the position of your golden Bauble
	 */
	public Point getGoldenBaublePosition() { return new Point(POSITION); }
}
