package ihs.apcs.spacebattle.commands;

/**
 * A command to fire a ship's thrusters, gradually increasing its speed.
 * Each ship has four thrusters (back, front, left, right) that, when fired,
 *   propel the ship in the opposite direction (e.g. firing the back thruster 
 *   moves a ship forward).  Ships have a finite amount of thruster power that
 *   cannot be exceeded by the combined power of the four thrusters.
 * @author Brett Wortzman
 *
 * @since 0.1
 * @version 1.1
 */
public class ThrustCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private char DIR;
	@SuppressWarnings("unused")
	private double DUR;
	@SuppressWarnings("unused")
	private double PER;
	
	/**
	 * Creates a command to fire a ship's thrusters.  If the ship does not have
	 *   enough thruster power remaining to execute a thrust, it is ignored.
	 * @param dir which thruster to fire (one of 'B', 'F', 'L', 'R')
	 * @param duration the number of seconds to thrust
	 * @param power the percentage of thruster power to be used for this thrust
	 */
	public ThrustCommand(char dir, double duration, double power) {
		if (dir != 'L' && dir != 'F' && dir != 'R' && dir != 'B')
			throw new IllegalArgumentException("Invalid thrust direction; must be one of 'L', 'F', 'R', or 'B'");
		if (power < 0.1 || power > 1.0)
			throw new IllegalArgumentException("Invalid thrust power: must be between 0.1 and 1.0");
		if (duration < 0.1)
			throw new IllegalArgumentException("Invalid thrust duration: must be at least 0.1");
		
		DIR = dir;
		DUR = duration;
		PER = power;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Thrust.toString();
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (3)
	 */
	public static int getOngoingEnergyCost() { return 3; }
	
	/**
	 * Thrust commands don't prevent you from executing other commands.
	 * 
	 * If you want to wait for the Thrust to complete, you should issue an Idle command during your next cycle.
     *
     * @since 1.1
	 * @return false, thrusting doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
