package ihs.apcs.spacebattle.commands;

/**
 * A command to fire a torpedo.  Torpedos can be fired from either the front or
 *   back of a ship.
 * @author Brett Wortzman
 *
 */
public class FireTorpedoCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private char DIR;

	/**
	 * Creates a command to fire a torpedo.
	 * @param direction which launcher to fire from ('F' for front, 'B' for back)
	 */
	public FireTorpedoCommand(char direction) {
		this.DIR = direction;
	}
	
	@Override
	protected String getName() {
		// TODO Auto-generated method stub
		return "FIRE";
	}
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (12)
	 */
	public static int getInitialEnergyCost() { return 12; }
	
	/**
	 * Fire Torpedo executes immediately.
	 * 
	 * @since 2.0
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
