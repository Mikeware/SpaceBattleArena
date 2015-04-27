package ihs.apcs.spacebattle.networking;

import java.util.HashMap;

public class ErrorData {
	private String COMMAND;
	private HashMap<String, Object> PARAMETERS;
	private String MESSAGE;
	
	public String toString() {
		return String.format("ERROR: Command %s(%s) failed: %s", COMMAND, PARAMETERS, MESSAGE);
	}
}
