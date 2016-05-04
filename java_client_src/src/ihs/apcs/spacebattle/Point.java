package ihs.apcs.spacebattle;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a point in space as an (x, y) coordinate.
 * @author Brett Wortzman
 * 
 * @since 0.1
 * @version 1.2
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
	 * 
	 * @version 1.2
	 */
	public int getAngleTo(Point other) {		
		double xDiff = other.getX() - this.getX();
		double yDiff = -1 * (other.getY() - this.getY()); // Our coordinates are flipped compared to regular math functions.
		
		return (int)Math.round(Math.toDegrees(Math.atan2(yDiff, xDiff)) + 360) % 360;
	}
	
	/**
	 * Returns a new point which represents the location at the given angle and distance away from this point.
	 * 
	 * @param angle from due east (0 degrees)
	 * @param distance from this point
	 * @return a new Point the given angle/distance away from this point
	 * 
	 * @since 1.2
	 */
	public Point getPointFromAngleAndDistance(double angle, double distance)
	{
		return new Point(this.getX() + distance * Math.cos(Math.toRadians(angle)), 
						 this.getY() - distance * Math.sin(Math.toRadians(angle)));
	}
	
	/**
	 * Checks if this point is in an Ellipse with the given center point, major/minor axis lengths and orientation.
	 * 
	 * @param center of the ellipse
	 * @param major axis length
	 * @param minor axis length
	 * @param orientation angle of the major axis
	 * @return true if this point is within the specified ellipse
	 * 
	 * @since 1.2
	 */
	public boolean inEllipse(Point center, int major, int minor, int orientation)
	{
		double xDiff = this.getX() - center.getX();
		double yDiff = -1 * (this.getY() - center.getY()); // Our coordinates are flipped compared to regular math functions.
		
		double cos = Math.cos(Math.toRadians(orientation));
		double sin = Math.sin(Math.toRadians(orientation));

		return (Math.pow(cos * xDiff + sin * yDiff, 2) / (major * major)) +
			   (Math.pow(sin * xDiff - cos * yDiff, 2) / (minor * minor)) <= 1;
	}
	
	/**
	 * Wraps this point on a torus of size width, height if the point is within the given tolerance of the edge of the Torus.
	 * 
	 * Returns a List of points (including this one) which represent the coordinates of this point projected beyond the bounds of the 'world' on a Torus.
	 * This can be used to determine if a point is actually close to a position when it exists beyond the bounds of the 'world'.
	 * 
	 * @param width of torus
	 * @param height of torus
	 * @param tolerance to wrap coordinates
	 * @return set of points projected beyond bounds of torus
	 * 
	 * @since 1.2
	 */
	public List<Point> getPointsOnTorus(int width, int height, int tolerance)
	{
		List<Point> points = new ArrayList<Point>();
		points.add(new Point(this.getX(), this.getY()));
		
		if (this.getX() < tolerance) {
			if (this.getY() < tolerance) {
				points.add(new Point(this.getX() + width, this.getY() + height));
			}
			
			points.add(new Point(this.getX() + width, this.getY()));				
		} else if (this.getX() > width - tolerance) {
			if (this.getY() > height - tolerance) {
				points.add(new Point(this.getX() - width, this.getY() - height));
			}
			
			points.add(new Point(this.getX() - width, this.getY()));
		}
		
		if (this.getY() < tolerance) {
			points.add(new Point(this.getX(), this.getY() + height));				
		} else if (this.getY() > height - tolerance) {
			points.add(new Point(this.getX(), this.getY() - height));
		}
		
		return points;
	}
	
	/**
	 * Returns true if the given point's X & Y values are within the tolerance of this point's X & Y values.
	 * This is a 'box' test.
	 * 
	 * @param other location to test against
	 * @param tolerance amount to test in range against
	 * @return true if the points are close to one another.
	 * 
	 * @since 1.2
	 */
	public boolean closeTo(Point other, double tolerance)
	{
		return (Math.abs(this.getX() - other.getX()) <= tolerance &&
				Math.abs(this.getY() - other.getY()) <= tolerance);
	}
	
	public String toString() {
		return String.format("(%f, %f)", getX(), getY());
	}
		
	public boolean equals(Point other) {
		return (this.getX() == other.getX() && this.getY() == other.getY());
	}
}
