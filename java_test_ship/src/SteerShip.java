import java.awt.Color;

import ihs.apcs.spacebattle.*;
import ihs.apcs.spacebattle.commands.*;

/**
 * Example 'Dummy' Ship for Basic Connection with no Game.
 * 
 * @author Michael A. Hawker
 *
 */
public class SteerShip extends BasicSpaceship {

	public static void main(String[] args) {
		ihs.apcs.spacebattle.TextClient.main(new String[] {"127.0.0.1", "SteerShip"});		
	}
	
	private int current = -1;
	
	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.Spaceship#registerShip(int, int, int)
	 */
	@Override
	public RegistrationData registerShip(int numImages, int worldWidth,
			int worldHeight) {
		return new RegistrationData("Steer Ship", new Color(255, 0, 0), 0);
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.Spaceship#getNextCommand(ihs.apcs.spacebattle.Environment)
	 */
	@Override
	public ShipCommand getNextCommand(BasicEnvironment env) {
		current++;
		switch (current)
		{
			case 0:
				return new ThrustCommand('B', 3.0, 1.0);
			case 1:
				return new IdleCommand(5.0);
			case 2:
				return new SteerCommand(90, false);
			case 3:
				current = -1;
				return new SteerCommand(-45);
		}
		
		return new IdleCommand(5.0);
	}

	/* (non-Javadoc)
	 * @see ihs.apcs.spacebattle.Spaceship#shipDestroyed()
	 */
	@Override
	public void shipDestroyed(String lastDestroyedBy) {
		// TODO Auto-generated method stub

	}

}
