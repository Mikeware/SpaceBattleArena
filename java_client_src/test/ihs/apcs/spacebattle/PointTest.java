package ihs.apcs.spacebattle;

import java.util.Random;

import org.junit.Assert;
import org.junit.Test;

/**
 * @author oshoukry
 */
public class PointTest {
	private static final Random RANDOM = new Random(System.currentTimeMillis());

	@Test
	public void samePointReturnsZero() {
		Point point = getPoint(1.0, 1.0);

		check(point, point, 0, 0);
	}

	@Test
	public void horizontalPoints() {
		Point first = getPoint(1.0, 1.0);
		Point second = getPoint(2.0, 1.0);

		check(first, second, 0, 180);
	}

	@Test
	public void verticalPoints() {
		Point first = getPoint(1.0, 1.0);
		Point second = getPoint(1.0, 2.0);

		check(first, second, 90, 270);
	}

	@Test
	public void firstQuadrant45Degrees() {
		Point first = getPoint(1.0, 1.0);
		Point second = getPoint(2.0, 2.0);

		check(first, second, 45, 225);
	}

	@Test
	public void firstQuadrantNegative45Degrees() {
		Point first = getPoint(2.0, 2.0);
		Point second = getPoint(1.0, 3.0);

		check(first, second, 135, 315);
	}

	@Test
	public void exhaustiveFullCircleCounterClockwise() {
		for(int i = 0; i < 360; i++) {
			Point first = anyPoint();
			Point second = getPointUsingDistanceAndAngle(first, anyDistance(), i);
			check(first, second, i, (180 + i) % 360);
		}
	}

	@Test
	public void exhaustiveFullCircleClockwise() {
		for(int i = -360; i < 0; i++) {
			Point first = anyPoint();
			Point second = getPointUsingDistanceAndAngle(first, anyDistance(), i);
			check(first, second, 360 + i, (540 + i) % 360);
		}
	}

	private void check(Point first, Point second, int firstToSecond, int secondToFirst) {
		Assert.assertEquals("First " + first + " -> Second " + second, firstToSecond, first.getAngleTo(second));
		Assert.assertEquals("Second " + second + " -> First " + first, secondToFirst, second.getAngleTo(first));
	}

	private Point anyPoint() {
		return new Point(RANDOM.nextDouble() * 200 - 100.0, RANDOM.nextDouble() * 200 - 100);
	}

	private double anyDistance() {
		return RANDOM.nextInt(100) + 1;
	}

	private Point getPointUsingDistanceAndAngle(Point current, double distance, final double angle) {
		final double deltaX = Math.cos(Math.toRadians(angle));
		final double deltaY = Math.sin(Math.toRadians(angle));

		double newX = current.getX() + distance * deltaX;

		double newY = current.getY() + distance * deltaY;
		return new Point(newX, newY);
	}

	@Test
	public void checkPointPosition() {
		Point first = new Point(1, 1);
		Point second = getPointUsingDistanceAndAngle(first, Math.sqrt(2), 45);
		Assert.assertEquals(second.getX(), 2.0, 0.0);
		Assert.assertEquals(second.getY(), 2.0, 0.0);
	}

	private Point getPoint(double x, double y) {
		return new Point(x, y);
	}
}