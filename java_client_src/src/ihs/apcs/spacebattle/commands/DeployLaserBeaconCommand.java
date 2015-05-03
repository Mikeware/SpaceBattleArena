package ihs.apcs.spacebattle.commands;

/**
 * A command to deploy a laser beacon from a ship.  
 * <p>
 * Pairs of laser beacons draw a line in space.  The first beacon deployed
 *   represents the starting point of the line; the next beacon will terminate
 *   the line.  Lines do not follow the ship's path-- they simply connect two
 *   beacons directly.
 * @author Brett Wortzman
 *
 */
public class DeployLaserBeaconCommand extends ShipCommand {

	/**
	 * Creates a command to deploy a laser beacon at the ship's current
	 *   position.
	 */
	@Override
	protected String getName() {
		return "DLBN";
	}

	/**
	 * Deploy Laser Beacons executes immediately.
	 * 
	 * @since 2.0
	 * @return
	 */
	public static boolean executesImmediately() { return true; }
}
