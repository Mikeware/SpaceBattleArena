/**
 * 
 */
package ihs.apcs.spacebattle.util;

import java.util.HashMap;
import java.util.Map;

/**
 * @author Brett Wortzman
 *
 */
public class StringMap<T> extends HashMap<String, T> {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6086952182878503256L;

	/**
	 * 
	 */
	public StringMap() {
		// TODO Auto-generated constructor stub
	}

	/**
	 * @param arg0
	 */
	public StringMap(int arg0) {
		super(arg0);
		// TODO Auto-generated constructor stub
	}

	/**
	 * @param arg0
	 */
	public StringMap(Map<? extends String, ? extends T> arg0) {
		super(arg0);
		// TODO Auto-generated constructor stub
	}

	/**
	 * @param arg0
	 * @param arg1
	 */
	public StringMap(int arg0, float arg1) {
		super(arg0, arg1);
		// TODO Auto-generated constructor stub
	}

}
