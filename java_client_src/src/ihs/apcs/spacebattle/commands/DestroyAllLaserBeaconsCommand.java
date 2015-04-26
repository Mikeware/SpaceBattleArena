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

}
