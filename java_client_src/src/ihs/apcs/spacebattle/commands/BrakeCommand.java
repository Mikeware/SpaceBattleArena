/**
 * 
 */
package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to gradually slow down from its current speed.
 * @author Brett Wortzman
 * 
 * @since 0.1
 * @version 0.1
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
		if (power < 0.0 || power >= 1.0)
			throw new IllegalArgumentException("Invalid brake power: must be at least 0.0 and less than 1.0");
		
		PER = power;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Brake.toString();
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (4)
	 */
	public static int getOngoingEnergyCost() { return 4; }
}
