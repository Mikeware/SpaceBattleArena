package ihs.apcs.spacebattle.commands;

import ihs.apcs.spacebattle.util.StringMap;

/**
 * A command to warp a ship.  Warping moves a ship a great distance in a short period
 * of time.  Warping can be done in one of two ways:
 * <ul>
 * 	<li>A "random warp" that warps a ship a random distance in a random direction</li>
 * 	<li>A "directed warp" that warps a ship a given distance in the direction it is currently facing</li>
 * </ul>
 * Warping is delayed by 1 second (while the warp drive warms up) and requires a cool-down period after the
 * warp is completed.  The cool-down period and energy cost of a warp vary based on the type and distance.
 * @author Brett Wortzman
 *
 */
public class WarpCommand extends ShipCommand {
	private double DIST;
	
	/**
	 * Creates a random warp command.
	 * <p>
	 * The ship will be warped a random distance up to 1000 pixels both horizontally and vertically.
	 * A random warp has a cool-down period of 5 seconds.
	 */
	public WarpCommand() { }
	
	/**
	 * Creates a directed warp command.
	 * <p>
	 * The ship will be warped the given distance (maximum of 400 pixels) in the direction the ship is
	 * currently facing.  A directed warp has a cool-down period of {@code distance / 50}. 
	 * @param distance the distance to warp (maximum 400)
	 */
	public WarpCommand(double distance) {
		this.DIST = distance;
	}

	@Override
	protected String getName() {
		return "WARP";
	}
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (10)
	 */
	public static int getInitialEnergyCost() { return 10; }
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (9)
	 */
	public static int getOngoingEnergyCost() { return 9; }
	
	protected StringMap<Object> getArgs() throws IllegalArgumentException, IllegalAccessException {
		if (DIST > 0) {
			return super.getArgs();
		} else {
			return new StringMap<Object>();
		}
	}

}
