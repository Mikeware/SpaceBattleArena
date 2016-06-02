package ihs.apcs.spacebattle.commands;

/**
 * A command to deploy a Space Mine.  Space Mines will remain inactive for a period of time.  Once active, they will explode on impact.
 * 
 * Space Mines have three modes:
 *  Stationary (will activate after given time and remain in place) and cost 44 energy.
 *  Autonomous (will activate, boost in the given direction and speed, and then detonate after the given period of time) and cost 55 energy.
 *  Homing (will activate after the given time and then start tracking nearby ships) and cost 66 energy.
 * 
 * @author Michael A. Hawker
 *
 * @since 1.2
 * @version 1.2
 */
public class DeploySpaceMineCommand extends ShipCommand {
	private int MODE;
	@SuppressWarnings("unused")
	private double DELAY;
	@SuppressWarnings("unused")
	private int DIR;
	@SuppressWarnings("unused")
	private int SPEED;
	@SuppressWarnings("unused")
	private double DUR;

	/**
	 * Creates a command to deploy a stationary space mine.
	 * @param delay time to wait before becoming active.
	 */
	public DeploySpaceMineCommand(double delay)
	{
		this(delay, false);
	}
	
	/**
	 * Creates a command to deploy a space mine which is either stationary or homing.
	 * @param delay time to wait before becoming active.
	 * @param homing does this mine home nearby ships.
	 */
	public DeploySpaceMineCommand(double delay, boolean homing) {
		if (delay <= 0 || delay > 10) 
			throw new IllegalArgumentException("Invalid mine delay: must be greater than 0 and no more than 10");
		
		if (homing)
		{
			this.MODE = 3;
		}
		else 
		{
			this.MODE = 1;
		}
		this.DELAY = delay;
	}
	
	/**
	 * Create a command to deploy a space mine which will move after the given time in a direction with some amount of speed and then explode.
	 * @param delay time before becoming active and applying initial movement
	 * @param direction to move in after delay
	 * @param speed (1-5) speed factor
	 * @param duration after becoming active, how long until the mine explodes
	 */
	public DeploySpaceMineCommand(double delay, int direction, int speed, double duration)
	{
		if (duration <= 0 | duration > 10)
			throw new IllegalArgumentException("Invalid mine duration: must be greater than 0 and no more than 10");
		if (speed <= 0 || speed > 5)
			throw new IllegalArgumentException("Invalid mine speed: must be between 1 and 5 inclusive");
		if (delay <= 0 || delay > 10) 
			throw new IllegalArgumentException("Invalid mine delay: must be greater than 0 and no more than 10");
		
		this.MODE = 2;
		this.DELAY = delay;
		this.DIR = direction;
		this.SPEED = speed;
		this.DUR = duration;
	}
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.DeploySpaceMine.toString();
	}
	
	/**
	 * Gets the energy cost for the constructed command.
	 * @return (33, 44, 55)
	 */
	public int getEnergyCost()
	{
		return 22 + this.MODE * 11;
	}
	
	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (33, 44, or 55)
	 */
	public static int getInitialEnergyCost() { return 33; }
	
	/**
	 * Deploy Space Mine executes immediately and has a cooldown of 2 seconds.
	 * 
	 * @return true
	 */
	public static boolean executesImmediately() { return true; }
}
