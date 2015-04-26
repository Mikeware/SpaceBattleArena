/**
 * 
 */
package ihs.apcs.spacebattle;

/**
 * @author Brett Wortzman
 *
 */
public class Pair<T, U> {
	private T first;
	private U second;
	
	public Pair(T first, U second) {
		this.first = first;
		this.second = second;
	}
	
	public T getFirst()  { return first; }
	public U getSecond() { return second; }
	
	public String toString() {
		return String.format("(%s, %s)", first.toString(), second.toString());
	}
}
