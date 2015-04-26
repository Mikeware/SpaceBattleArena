package ihs.apcs.spacebattle;

import ihs.apcs.spacebattle.networking.MwnpMessage;

import java.io.IOException;

public interface Client {
	public void disconnect() throws IOException;
	public <T> void parseMessage(MwnpMessage msg) throws IOException, IllegalArgumentException, IllegalAccessException;
	public void logMessage(String message);
}
