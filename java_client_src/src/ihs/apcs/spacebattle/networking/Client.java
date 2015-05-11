package ihs.apcs.spacebattle.networking;

import java.io.IOException;

public interface Client {
	public boolean isDisconnected();
	public void disconnect() throws IOException;
	public <T> void parseMessage(MwnpMessage msg) throws IOException, IllegalArgumentException, IllegalAccessException;
	public void logMessage(String message);
}
