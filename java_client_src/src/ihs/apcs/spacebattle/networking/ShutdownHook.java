/**
 * 
 */
package ihs.apcs.spacebattle.networking;

import java.io.IOException;

/**
 * @author Brett Wortzman
 *
 */
public class ShutdownHook extends Thread {
	private Client client;
	
	public ShutdownHook(Client client) {
		this.client = client;
	}
	
	public void run() { 
		try {
			System.out.println("Shutting down...");
			if (!client.isDisconnected())
			{
				client.disconnect();
			}
		} catch (IOException e) {
			System.err.println("Shutdown error...");
			System.err.println(e.getMessage());
			e.printStackTrace();
		} 
	}
}
