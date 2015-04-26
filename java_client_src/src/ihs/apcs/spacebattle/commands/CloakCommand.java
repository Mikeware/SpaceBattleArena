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
 */
public class CloakCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private double DUR;
	
	/**
	 * Creates a command to cloak a ship.
	 * @param duration the amount of time to remain cloaked (in seconds)
	 */
	public CloakCommand(double duration)  {
		this.DUR= duration;
	}
	
	@Override
	protected String getName() {
		return "CLOAK";
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
}
