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
 * <table border="1" summary="Table of Radar Levels and Behavior">
 * <tr><th>Level</th><th>Duration</th><th>Information Gathered</th></tr>
 * <tr><td>1</td><td>0.03 s</td><td>None (number of objects only)</td></tr>
 * <tr><td>2</td><td>0.10 s</td><td>ID# and position</td></tr>
 * <tr><td>3</td><td>0.10 s</td><td>All (for specified target only)</td></tr>
 * <tr><td>4</td><td>0.15 s</td><td>ID#, position, type</td></tr>
 * <tr><td>5</td><td>0.40 s</td><td>All</td></tr>
 * </table>
 * 
 * <p>Performing a RadarCommand will populate the {@link ihs.apcs.spacebattle.Environment#getRadar()} method's results 
 * on the next call to {@link ihs.apcs.spacebattle.Spaceship#getNextCommand(ihs.apcs.spacebattle.Environment)} and only the next call.
 * Results need to be saved to be compared to future Radar sweeps.
 *
 * @author Brett Wortzman
 * @since 0.1
 * @version 0.1
 */
public class RadarCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private int LVL;
	@SuppressWarnings("unused")
	private int TARGET;
	
	/**
	 * Creates a command to perform a radar sweep of the specified level.
	 * Blocks for the amount of time specified above.
	 * @param level the level of sweep to perform
	 */
	public RadarCommand(int level) {
		if (level < 1 || level > 5 || level == 3)
			throw new IllegalArgumentException("Invalid radar level: must be 1, 2, 4, or 5");
		
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
			throw new IllegalArgumentException("Invalid radar level: only radar level 3 accepts a target");
		if (target <= 0)
			throw new IllegalArgumentException("Invalid radar target: must be positive integer");
		
		this.LVL = level;
		this.TARGET = target;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.Radar.toString();
	}

	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (6)
	 */
	public static int getOngoingEnergyCost() { return 6; }
}
