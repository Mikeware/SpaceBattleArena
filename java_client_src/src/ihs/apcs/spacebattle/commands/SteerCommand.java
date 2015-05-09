package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to change its course by the amount indicated.  Positive values adjust 
 *   counter-clockwise; negative values adjust clockwise
 * @author Michael A. Hawker
 *
 */
public class SteerCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int DEG;
	
	/**
	 * Creates a command to steer a ship.  
	 * @param degrees the number of degrees to adjust course
	 */
	public SteerCommand(double degrees) {
		DEG = (int)degrees;
	}

	@Override
	protected String getName() {
		return "STEER";
	}
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (4)
	 */
	public static int getOngoingEnergyCost() { return 4; }
}
