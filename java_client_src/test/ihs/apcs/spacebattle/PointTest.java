package ihs.apcs.spacebattle;

import static org.junit.Assert.*;

import java.util.List;

import junit.framework.Assert;

import org.junit.Test;

public class PointTest {

	@Test
	public void testGetDistanceTo() {
		Point one = new Point(0, 0);
		Point two = new Point(100, 100);
		Point three = new Point(-100, 100);
		
		assertEquals(Math.sqrt(2 * 100 * 100), one.getDistanceTo(two), 0.1);
		assertEquals(200, two.getDistanceTo(three), 0.01);
	}

	@Test
	public void testGetAngleTo() {
		assertEquals(45, (new Point(0, 0)).getAngleTo(new Point(1, -1)), 0.01);
		
		for (int i = 0; i < 360; i++)
		{
			Point zero = new Point(0, 0);
			// - Y as our coordinate system is flipped
			Point loc = new Point(Math.cos(Math.toRadians(i)), -Math.sin(Math.toRadians(i)));
			//System.out.println(i + ", " + ((zero.getAngleTo(loc) + 360) % 360));
			assertEquals(i, zero.getAngleTo(loc));
		}
	}
	
	@Test
	public void testGetPointFromAngleAndDistance() {
		assertTrue((new Point(0, 0)).getPointFromAngleAndDistance(45, 10).closeTo(new Point(7.07, -7.07), 0.1));
		assertTrue((new Point(0, 0)).getPointFromAngleAndDistance(135, 10).closeTo(new Point(-7.07, -7.07), 0.1));
		assertTrue((new Point(0, 0)).getPointFromAngleAndDistance(-45, 10).closeTo(new Point(7.07, 7.07), 0.1));
		
		for (int i = 0; i < 360; i++)
		{
			Point zero = new Point(0, 0);
			Point loc = zero.getPointFromAngleAndDistance(i, 1);
			assertTrue(loc.closeTo(new Point(Math.cos(Math.toRadians(i)), -Math.sin(Math.toRadians(i))), 0.05));
		}
	}
	
	@Test
	public void testInEllipse() {
		// Test Basic Points Edges in Standard Ellipse
		assertTrue((new Point(0, 1)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(0, -1)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(0, -1.01)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(0, 0)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(4, 1)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(4, 0)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(-4, 0)).inEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(-4.01, 0)).inEllipse(new Point(0, 0), 4, 1, 0));
		
		// Test Rotation
		assertFalse((new Point(-1, -1)).inEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(1, -1)).inEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(-1, 1)).inEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(1, 1)).inEllipse(new Point(0, 0), 2, 1, 0));
		assertTrue((new Point(1, 1)).inEllipse(new Point(0, 0), 2, 1, -45));
		assertFalse((new Point(1, -1)).inEllipse(new Point(0, 0), 2, 1, -45));
		assertTrue((new Point(-1, -1)).inEllipse(new Point(0, 0), 2, 1, -45));
		assertFalse((new Point(1, 1)).inEllipse(new Point(0, 0), 2, 1, 45));
	}
	
	@Test
	public void testGetPointsOnTorus() {
		// TODO: deal with checking actual results
		List<Point> points = (new Point(5.0, 5.0)).getPointsOnTorus(200, 100, 10);
		
		assertEquals(4, points.size());
		
		System.out.println(points);
		
		points = (new Point(15.0, 5.0)).getPointsOnTorus(200, 100, 10);
		
		assertEquals(2, points.size());
		
		System.out.println(points);
		
		points = (new Point(15.0, 15.0)).getPointsOnTorus(200, 100, 10);
		
		assertEquals(1, points.size());
		
		System.out.println(points);
	}

	@Test
	public void testEqualsPoint() {
		Point one = new Point(25.0, 50.0);
		Point two = new Point(25, 50);
		Point three = new Point(50, 25);
		
		assertTrue(one.equals(two));
		assertFalse(two.equals(three));
		assertFalse(one.equals(new Point(25.000001, 50.0)));
	}

	@Test
	public void testCloseTo()
	{
		Point one = new Point(25.1, 49.9);
		Point two = new Point(24.9, 50.1);
		
		assertTrue(one.closeTo(two, 0.20001));
		assertFalse(one.closeTo(two, 0.1));
	}
}
