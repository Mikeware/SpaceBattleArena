/**
 * 
 */
package ihs.apcs.spacebattle.commands;

/**
 * A "Discovery Quest" specific command to perform research on a specific object.
 * <p>
 * An id of a nearby object to scan is required and must be within a third of your radar range for a full duration of 2.5 seconds in order to be successfully scanned.
 *
 * <p>Scanning is a non-blocking operation.
 * 
 * @author Michael A. Hawker
 * @since 1.1
 * @version 1.1
 */
public class ScanCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int TARGET;
	
	/**
	 * Creates a command to perform a research scan of a specific object.
	 * @param target id number of the object to scan.
	 */
	public ScanCommand(int target) {
		this.TARGET = target;
	}
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	protected String getName() {
		return "DQSCN";
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (4)
	 */
	public static int getInitialEnergyCost() { return 4; }	
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (4)
	 */
	public static int getOngoingEnergyCost() { return 4; }
	
	/**
	 * Scanning does not block the processing of other commands.
	 * 
	 * @return false, scanning doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
