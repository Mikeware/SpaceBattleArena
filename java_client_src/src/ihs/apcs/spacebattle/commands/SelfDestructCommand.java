package ihs.apcs.spacebattle.commands;

/**
 * A command to "self-destruct" a ship by disconnecting it from the server.
 * <p>
 * <i>Note: This command is not actually sent to the server.  It is intercepted by the
 *          client and interpreted as a request to disconnect rather than send a new command.</i>
 * @author Brett Wortzman
 *
 */
public class SelfDestructCommand extends ShipCommand {
	
	/**
	 * Creates a command to "self-destruct" a ship.
	 */
	public SelfDestructCommand() { }

	@Override
	protected String getName() {
		// TODO Auto-generated method stub
		return "SELFDEST";
	}

}
