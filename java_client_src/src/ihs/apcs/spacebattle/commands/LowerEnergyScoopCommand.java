package ihs.apcs.spacebattle.commands;

import ihs.apcs.spacebattle.commands.ShipCommand;

/**
 * The LowerEnergyScoopCommand deploys an energy collector under your ship.
 * <p>If flying through a celestial body (like a Sun or Nebula), this scoop will collect a massive amount of energy.
 * It will additionally cause some drag.
 *
 * <p>If not in an energy source, this command will drain energy quickly.
 * 
 * <p>It can be run for a 'short period' of 3 seconds or a 'long period' of 6 seconds.  A long period will restore almost all energy from the initial requirements to start this command (4).
 * 
 * <p>Scooping is a non-blocking operation.
 * 
 * @author Michael A. Hawker
 *
 * @since 1.1
 * @version 1.1
 */
public class LowerEnergyScoopCommand extends ShipCommand {
	@SuppressWarnings("unused")
	private boolean SHORT;
	
	/**
	 * Creates a command to lower your energy scoop to recharge your ships energy in a Nebula or Star.
	 * @param shortlength indicates if you want to recharge for 3 (true) or 6 (false) seconds.
	 */
	public LowerEnergyScoopCommand(boolean shortlength) {
		this.SHORT = shortlength;
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.commands.ShipCommand#getName()
	 */
	@Override
	public String getName() {
		return CommandNames.LowerEnergyScoop.toString();
	}

	/**
	 * Gets the one-time energy cost to initiate this command.
	 * @return the amount of energy consumed by initiating this command (4)
	 */
	public static int getInitialEnergyCost() { return 4; }
	
	/**
	 * Gets the energy cost per second of this command.
	 * @return the amount of energy consumed per second while this command is executing (8)
	 */
	public static int getOngoingEnergyCost() { return 8; }	
	
	/**
	 * Scooping does not block the processing of other commands.
	 * 
	 * @return false, scooping doesn't block.
	 */
	public static boolean isBlocking() { return false; }
}
