package ihs.apcs.spacebattle.commands;

/**
 * "The Hunger Baubles" specific command to eject the specified Bauble from your ship's cargo hold.
 * <p>
 * An id of a bauble is required and must be contained within your ship.  See {@link ihs.apcs.spacebattle.games.TheHungerBaublesGameInfo#getBaublesInCargo()}.
 *
 * @author Michael A. Hawker
 *
 * @since 1.2
 * @version 1.2
 */
public class EjectCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int ID;

	/**
	 * Creates a command to drop the specified Bauble.
	 * @param target id number of the bauble.
	 */
	public EjectCommand(int target) {
		this.ID = target;
	}
		
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Eject.toString();
	}
	
	/**
	 * Gets the energy cost for the constructed command.
	 * @return (3 * baubleValue)
	 */
	public int getEnergyCost(int baubleValue)
	{
		return 3 * baubleValue;
	}
	
	/**
	 * Gets the average one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (3 * Bauble Value)
	 */
	public static int getInitialEnergyCost() { return 12; }
	
	/**
	 * Ejecting Baubles executes immediately after a cooldown of 0.5 seconds * mass of Bauble to eject.
	 * 
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
