package ihs.apcs.spacebattle;

import static org.junit.Assert.*;

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
		Point zeropt = new Point(0, 0);
		assertEquals(0, zeropt.getAngleTo(zeropt));
		assertEquals(45, zeropt.getAngleTo(new Point(1, -1)), 0.01);
		
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
		assertTrue((new Point(0, 0)).getPointAt(45, 10).isCloseTo(new Point(7.07, -7.07), 0.1));
		assertTrue((new Point(0, 0)).getPointAt(135, 10).isCloseTo(new Point(-7.07, -7.07), 0.1));
		assertTrue((new Point(0, 0)).getPointAt(-45, 10).isCloseTo(new Point(7.07, 7.07), 0.1));
		
		for (int i = 0; i < 360; i++)
		{
			Point zero = new Point(0, 0);
			Point loc = zero.getPointAt(i, 1);
			assertTrue(loc.isCloseTo(new Point(Math.cos(Math.toRadians(i)), -Math.sin(Math.toRadians(i))), 0.05));
		}
	}
	
	@Test
	public void testIsInEllipse() {
		// Test Basic Points Edges in Standard Ellipse
		assertTrue((new Point(0, 1)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(0, -1)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(0, -1.01)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(0, 0)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(4, 1)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(4, 0)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertTrue((new Point(-4, 0)).isInEllipse(new Point(0, 0), 4, 1, 0));
		assertFalse((new Point(-4.01, 0)).isInEllipse(new Point(0, 0), 4, 1, 0));
		
		// Test Rotation
		assertFalse((new Point(-1, -1)).isInEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(1, -1)).isInEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(-1, 1)).isInEllipse(new Point(0, 0), 2, 1, 0));
		assertFalse((new Point(1, 1)).isInEllipse(new Point(0, 0), 2, 1, 0));
		assertTrue((new Point(1, 1)).isInEllipse(new Point(0, 0), 2, 1, -45));
		assertFalse((new Point(1, -1)).isInEllipse(new Point(0, 0), 2, 1, -45));
		assertTrue((new Point(-1, -1)).isInEllipse(new Point(0, 0), 2, 1, -45));
		assertFalse((new Point(1, 1)).isInEllipse(new Point(0, 0), 2, 1, 45));
	}
	
	@Test
	public void testGetClosestMappedPoint() {
		Point me = new Point(5, 5);
		
		assertTrue((new Point(-5, 5)).isCloseTo(me.getClosestMappedPoint(new Point(95, 5), 100, 100), 0.1));		
		assertEquals(10, me.getDistanceTo(me.getClosestMappedPoint(new Point(95, 5), 100, 100)), 0.1);
		
		assertTrue((new Point(-5, -5)).isCloseTo(me.getClosestMappedPoint(new Point(95, 95), 100, 100), 0.1));
		
		assertTrue((new Point(95, 5)).isCloseTo(me.getClosestMappedPoint(new Point(95, 5), 200, 100), 0.1));
		
		me = new Point(50, 10);
		
		assertTrue((new Point(95, 5)).isCloseTo(me.getClosestMappedPoint(new Point(95, 5), 100, 100), 0.1));
		
		assertTrue((new Point(50, -35)).isCloseTo(me.getClosestMappedPoint(new Point(50, 65), 100, 100), 0.1));
		assertTrue((new Point(50, 55)).isCloseTo(me.getClosestMappedPoint(new Point(50, 55), 100, 100), 0.1));

		me = new Point(95, 90);
		
		assertTrue((new Point(90, 75)).isCloseTo(me.getClosestMappedPoint(new Point(90, 75), 100, 100), 0.1));
		assertTrue((new Point(110, 120)).isCloseTo(me.getClosestMappedPoint(new Point(10, 20), 100, 100), 0.1));
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
	public void testIsCloseTo()
	{
		Point one = new Point(25.1, 49.9);
		Point two = new Point(24.9, 50.1);
		
		assertTrue(one.isCloseTo(two, 0.20001));
		assertFalse(one.isCloseTo(two, 0.1));
	}
}
