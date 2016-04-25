package ihs.apcs.spacebattle;

/**
 * Represents a point in space as an (x, y) coordinate.
 * @author Brett Wortzman
 * 
 * @since 0.1
 * @version 0.1
 */
public class Point {
	private double x;
	private double y;
	
	/**
	 * Creates a new point with the given coordinates.
	 * @param x the x-coordinate
	 * @param y the y-coordinate
	 */
	public Point(double x, double y) {
		this.x = x;
		this.y = y;
	}
	
	/**
	 * Creates a new point from an array.  The first element of the array is
	 *   considered to be the x-coordinate and the second element is the 
	 *   y-coordinate.
	 * @param coords the coordinates of the point
	 */
	public Point(double[] coords) {
		this.x = coords[0];
		this.y = coords[1];
	}
	
	/**
	 * Gets the x-coordinate of this point.
	 * @return the x-coordinate
	 */
	public double getX() { return x; }
	
	/**
	 * Gets the y-coordinate of this point.
	 * @return the y-coordinate
	 */
	public double getY() { return y; }
	
	/**
	 * Gets the distance from this to another Point in space using the
	 *   standard distance formula.
	 * @param other the location to which to calculate the distance
	 * @return the distance between this point and other
	 */
	public double getDistanceTo(Point other) {
		return Math.sqrt(Math.pow(other.getX() - this.getX(), 2) + Math.pow(other.getY() - this.getY(), 2));
	}
	
	/**
	 * Gets the absolute angle between this and another Point in space.
	 *   More specifically, calculates the counter-clockwise angle from due 
	 *   east (0 degrees) to a line containing both this and other.  
	 *   <p>
	 *   To determine the amount of rotation necessary to face the argument,
	 *     a ship's current {@link ObjectStatus#getOrientation() orientation} should be subtracted from the result 
	 *     of this method.
	 * @param other the location to which to calculate the angle
	 * @return the absolute angle from this to other 
	 */
	public int getAngleTo(Point other) {

		double xDiff = this.getX() - other.getX();
		double yDiff = this.getY() - other.getY();

		if (xDiff == 0 && yDiff == 0) // same point
			return 0;

		return (180 + (int) Math.round((Math.atan2(yDiff, xDiff) * 180 / Math.PI))) % 360;
	}

	public String toString() {
		return String.format("(%f, %f)", getX(), getY());
	}
	
	public boolean equals(Point other) {
		return (this.getX() == other.getX() && this.getY() == other.getY());
	}
}
