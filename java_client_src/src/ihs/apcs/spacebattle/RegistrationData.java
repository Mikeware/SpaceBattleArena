package ihs.apcs.spacebattle;

import java.awt.Color;

/**
 * Represents the data necessary for the server to register a new ship to begin
 * receiving commands.
 * @author Brett Wortzman
 *
 */
public class RegistrationData {
	private String NAME;
	private int[] COLOR;
	private int IMAGEINDEX;
	
	/**
	 * Creates a new RegistrationData object with the specified parameters.
	 * @param name the name to be associated with the ship being registered
	 * @param color the color for the ship to appear
	 * @param image the index of the image from the server's image list
	 * 			to be used for this ship
	 */
	public RegistrationData(String name, Color color, int image) {
		this.NAME = name;
		this.COLOR = new int[]{color.getRed(), color.getGreen(), color.getBlue()};
		this.IMAGEINDEX = image;
	}
	
	/**
	 * Gets the registered name.
	 * @return the name registered for the ship
	 */
	public String getName() { return NAME; }
	
	/**
	 * Gets the registered color.
	 * @return the color registered for the ship
	 */
	public Color getColor() { return new Color(COLOR[0], COLOR[1], COLOR[2]); }
	
	/**
	 * Gets the registered image index.
	 * @return the index of the image registered for the ship
	 */
	public int getImage() { return IMAGEINDEX; }
	
	public String toString() { 
		return String.format("[%s, [%d, %d, %d], %d]", getName(), getColor().getRed(), getColor().getGreen(), getColor().getBlue(), getImage());
	}
}
