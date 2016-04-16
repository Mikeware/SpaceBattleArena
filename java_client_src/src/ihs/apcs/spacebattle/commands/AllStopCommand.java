package ihs.apcs.spacebattle.commands;

/**
 * A command to bring a ship to an immediate full stop.
 * <p>
 * Will deplete energy by 40 and health by 50%.
 * @author Brett Wortzman
 *
 */
public class AllStopCommand extends ShipCommand {
	
	/**
	 * Creates a command to bring a ship to an immediate full stop.
	 */
	public AllStopCommand() { }

	@Override
	protected String getName() {
		return "STOP";
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (40)
	 */
	public static int getInitialEnergyCost() { return 40; }
	
	/**
	 * AllStop executes immediately.
	 * 
	 * @since 2.0
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
