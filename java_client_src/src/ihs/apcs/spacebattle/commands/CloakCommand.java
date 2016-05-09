package ihs.apcs.spacebattle.commands;

/**
 * A command to cloak a ship.  Ships that are cloaked are invisible to radar for
 *   a specified amount of time.  Ships will automatically decloak if they 
 *   raise shields or fire a torpedo.  Cloaking will fail (but still incur the 
 *   energy cost) if the ship's shields are up at the time of cloaking.  
 * <p>
 * Cloaking is a non-blocking operation.
 * @author Brett Wortzman
 *
 * @since 0.9
 * @version 1.1
 */
public class CloakCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private double DUR;
	
	/**
	 * Creates a command to cloak a ship.
	 * @param duration the amount of time to remain cloaked (in seconds)
	 */
	public CloakCommand(double duration)  {
		this.DUR = duration;
	}
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Cloak.toString();
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (15)
	 */
	public static int getInitialEnergyCost() { return 15; }
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (2)
	 */
	public static int getOngoingEnergyCost() { return 2; }
	
	/**
	 * Cloaking does not block the processing of other commands.
	 * 
	 * @since 1.1
	 * @return false, cloak doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
