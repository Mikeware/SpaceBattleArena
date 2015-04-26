/**
 * 
 */
package ihs.apcs.spacebattle.commands;

/**
 * A command to perform a radar sweep of the nearby area.
 * <p>
 * There are five levels of radar sweep that can be performed.  Higher levels
 * provide more information about objects in range, but also require more time.  
 * The levels are as follows:
 * <table border="1">
 * <tr><th>Level</th><th>Duration</th><th>Information Gathered</th></tr>
 * <tr><td>1</td><td>0.03 s</td><td>None (number of objects only)</td></tr>
 * <tr><td>2</td><td>0.10 s</td><td>ID# and position</td></tr>
 * <tr><td>3</td><td>0.10 s</td><td>All (for specified target only)</td></tr>
 * <tr><td>4</td><td>0.15 s</td><td>ID#, position, type</td></tr>
 * <tr><td>5</td><td>0.40 s</td><td>All</td></tr>
 * </table>
 *
 * @author Brett Wortzman
 */
public class RadarCommand extends ShipCommand {
	private int LVL;
	private int TARGET;
	
	/**
	 * Creates a command to perform a radar sweep of the specified level.
	 * Blocks for the amount of time specified above.
	 * @param level the level of sweep to perform
	 */
	public RadarCommand(int level) {
		this.LVL = level;
	}
	
	/**
	 * Creates a command to perform a targeted radar sweep to obtain full
	 *   details on a particular target.  This is a level 3 sweep.
	 * @param level the level of sweep to perform <b><i>(Must be 3)</i></b> 
	 * @param target the id number of the target to scan
	 */
	public RadarCommand(int level, int target) {
		if (level != 3)
			throw new IllegalArgumentException("Only radar level 3 accepts a target");
		
		this.LVL = level;
		this.TARGET = target;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	protected String getName() {
		return "RADAR";
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (6)
	 */
	public static int getOngoingEnergyCost() { return 6; }
}
