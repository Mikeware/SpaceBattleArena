package ihs.apcs.spacebattle.commands;

/**
 * A command to bring a ship to an immediate full stop.
 * <p>
 * Will deplete energy by 40 and health by 50% and wait for 5 seconds.
 * @author Brett Wortzman
 *
 * @since 0.9
 * @version 1.2
 */
public class AllStopCommand extends ShipCommand {
	
	/**
	 * Creates a command to bring a ship to an immediate full stop.
	 */
	public AllStopCommand() { }

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.AllStop.toString();
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (40)
	 */
	public static int getInitialEnergyCost() { return 40; }
	
	/**
	 * AllStop executes immediately and has a cooldown of 5 seconds.
	 * 
	 * @since 1.1
	 * @version 1.2
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
