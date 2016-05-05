package ihs.apcs.spacebattle.commands;

/**
 * A command to destroy all your laser beacons currently in space.  This
 *   has the effect of clearing all lines you have drawn.
 * @author Brett Wortzman
 *
 * @since 0.1
 * @version 1.1
 */
public class DestroyAllLaserBeaconsCommand extends ShipCommand {

	/**
	 * Creates a command to destroy all your laser beacons. 
	 */
	@Override
	protected String getName() {
		return "DAYLB";
	}
	
	/**
	 * Destroy Laser Beacons execute immediately.
	 * 
	 * @since 1.1
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
