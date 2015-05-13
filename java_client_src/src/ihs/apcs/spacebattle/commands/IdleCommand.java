/**
 * 
 */
package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to do nothing for a period of time.  Useful for
 *   waiting for non-blocking commands to finish or getting updated environment
 *   data without performing an action.
 * @author Brett Wortzman
 *
 */
public class IdleCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private double DUR;
	
	/**
	 * Creates a command to wait for a specified amount of time.  The ship
	 *   will not be able to act during this time.
	 * @param duration the number of seconds for which to idle
	 */
	public IdleCommand(double duration) {
		DUR = duration;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	protected String getName() {
		return "IDLE";
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (0)
	 */
	public static int getOngoingEnergyCost() { return 0; }
}
