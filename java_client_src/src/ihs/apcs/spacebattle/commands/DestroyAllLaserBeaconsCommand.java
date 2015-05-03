package ihs.apcs.spacebattle.commands;

/**
 * A command to destroy all your laser beacons currently in space.  This
 *   has the effect of clearing all lines you have drawn.
 * @author Brett Wortzman
 *
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
	 * @since 2.0
	 * @return
	 */
	public static boolean executesImmediately() { return true; }
}
