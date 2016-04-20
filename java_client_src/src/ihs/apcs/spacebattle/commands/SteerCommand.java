package ihs.apcs.spacebattle.commands;

/**
 * A command to cause a ship to change its course by the amount indicated.  Positive values adjust 
 *   counter-clockwise; negative values adjust clockwise.
 * <p>
 * Note: This does not adjust your ship's orientation to match, it only effects your movement direction. If you have no velocity, this command will have no effect.
 * <p>
 * Note: This command can be toggled with the optional second parameter to NOT block the ship, this is useful for performing more complex maneuvers.
 * @author Michael A. Hawker
 *
 * @since 1.0
 * @version 1.0.1
 */
public class SteerCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int DEG;
	@SuppressWarnings("unused")
	private boolean BLOCK;
	
	/**
	 * Creates a Blocking command to steer a ship.  
	 * @param degrees the number of degrees to adjust course
	 */
	public SteerCommand(double degrees) {
		this(degrees, true);
	}
	
	/**
	 * Creates a command to steer a ship.  
	 * @param degrees the number of degrees to adjust course
	 * @param block indicates if the command should block or not
	 */
	public SteerCommand(double degrees, boolean block) {
		DEG = (int)degrees;
		BLOCK = (boolean)block;
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
