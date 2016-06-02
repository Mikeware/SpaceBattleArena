package ihs.apcs.spacebattle.commands;

/**
 * "The Hunger Baubles" specific command to pick up the specified Bauble.
 * <p>
 * An id of the nearby bauble is required and must be within range to be picked up.
 *
 * @author Michael A. Hawker
 *
 * @since 1.2
 * @version 1.2
 */
public class CollectCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int ID;

	/**
	 * Creates a command to pick up the specified Bauble in range.
	 * @param target id number of the bauble.
	 */
	public CollectCommand(int target) {
		this.ID = target;
	}
		
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Collect.toString();
	}
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (8)
	 */
	public static int getInitialEnergyCost() { return 8; }
	
	/**
	 * Collecting Baubles executes immediately but has a cooldown of 0.2 seconds.
	 * 
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
