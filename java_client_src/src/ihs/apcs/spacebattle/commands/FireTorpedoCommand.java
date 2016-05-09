package ihs.apcs.spacebattle.commands;

/**
 * A command to fire a torpedo.  Torpedos can be fired from either the front or
 *   back of a ship.
 * @author Brett Wortzman
 *
 * @since 0.9
 * @version 1.1
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
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.FireTorpedo.toString();
	}
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (12)
	 */
	public static int getInitialEnergyCost() { return 12; }
	
	/**
	 * Fire Torpedo executes immediately.
	 * 
	 * @since 1.1
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
