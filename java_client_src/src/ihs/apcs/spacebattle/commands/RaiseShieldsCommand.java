package ihs.apcs.spacebattle.commands;

/**
 * A command to raise a ship's shields.  Shields will absorb 80% of damage from 
 *   weapons and collisions, protecting a ship's health.  Shields are limited and 
 *   once depleted will disengage and no longer provide protection.  While 
 *   shields are raised, they will be restored at a rate of 4 units per second up 
 *   to the maximum incurring an energy cost of 1 unit per second (in addition to 
 *   the normal energy cost).
 *   <p>
 *   Raising shields is a non-blocking operation.
 * @author Brett Wortzman
 *
 * @since 0.9
 * @version 1.1
 */
public class RaiseShieldsCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private double DUR;
	
	/**
	 * Creates a command to raise shields.
	 * @param duration the amount of time for which shields should be up (in seconds)
	 */
	public RaiseShieldsCommand(double duration) {
		this.DUR = duration;
	}

	@Override
	protected String getName() {
		// TODO Auto-generated method stub
		return "SHLD";
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (20)
	 */
	public static int getInitialEnergyCost() { return 20; }
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (4)
	 */
	public static int getOngoingEnergyCost() { return 4; }
	
	/**
	 * Raising Shields does not block the processing of other commands.
	 * 
     * @since 1.1
	 * @return false, raising shields doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
