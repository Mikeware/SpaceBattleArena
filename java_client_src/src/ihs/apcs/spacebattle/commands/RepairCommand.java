package ihs.apcs.spacebattle.commands;

import ihs.apcs.spacebattle.commands.ShipCommand;

/**
 * A command to repair a ship.  Repairing will restore a ship's health and shields at the expense of energy.
 * Both health and shields are restored at a rate of 4 units per second.
 * <p>
 * Repairing is a non-blocking operation.
 * @author Brett Wortzman
 *
 */
public class RepairCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int AMT;
	
	/**
	 * Creates a command to repair a ship.
	 * @param amount the amount of health to regenerate by repairing
	 */
	public RepairCommand(int amount) {
		this.AMT = amount;
	}

	@Override
	protected String getName() {
		return "REP";
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (8)
	 */
	public static int getOngoingEnergyCost() { return 8; }
	
	/**
	 * Repairing does not block the processing of other commands.
	 * 
	 * @since 2.0
	 * @return false, repairing doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
