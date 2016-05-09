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
 * @since 0.1
 * @version 1.1
 */
public class DeployLaserBeaconCommand extends ShipCommand {

	/**
	 * Creates a command to deploy a laser beacon at the ship's current
	 *   position.
	 */
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.DeployLaserBeacon.toString();
	}

	/**
	 * Deploy Laser Beacons executes immediately.
	 * 
	 * @since 1.1
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
