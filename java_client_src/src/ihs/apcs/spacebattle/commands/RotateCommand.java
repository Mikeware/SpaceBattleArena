package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to rotate.  Positive rotations are 
 *   counter-clockwise; negative rotations are clockwise
 * @author Brett Wortzman
 *
 */
public class RotateCommand extends ShipCommand {
	private int DEG;
	
	/**
	 * Creates a command to rotate a ship.  
	 * @param degrees the number of degrees to rotate
	 */
	public RotateCommand(double degrees) {
		DEG = (int)degrees;
	}

	@Override
	protected String getName() {
		return "ROT";
	}
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (2)
	 */
	public static int getOngoingEnergyCost() { return 2; }
}
