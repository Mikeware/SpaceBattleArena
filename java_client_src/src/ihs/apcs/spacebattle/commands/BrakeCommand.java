/**
 * 
 */
package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to gradually slow down from its current speed.
 * @author Brett Wortzman
 * 
 */
public class BrakeCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private double PER;
	
	
	/**
	 * Creates a command to gradually slow a ship to a percentage of its current speed.
	 *   The argument specifies the percentage of the ship's current speed to <i>maintain</i>.
	 *   For example, if 0.25 is passed, the ship will slow to 1/4 of its current speed.
	 * @param power the percentage of the ship's current speed to maintain
	 */
	public BrakeCommand(double power) {
		PER = power;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	protected String getName() {
		return "BRAKE";
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (4)
	 */
	public static int getOngoingEnergyCost() { return 4; }
}
