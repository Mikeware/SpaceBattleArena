package ihs.apcs.spacebattle.util;

public class Triple<T, U, V> {
	private T first;
	private U second;
	private V third;
	
	public Triple(T first, U second, V third) {
		this.first = first;
		this.second = second;
		this.third = third;
	}
	
	public T getFirst()  { return first; }
	public U getSecond() { return second; }
	public V getThird() { return third; }
	
	public String toString() {
		return String.format("(%s, %s, %s)", first.toString(), second.toString(), third.toString());
	}
}
