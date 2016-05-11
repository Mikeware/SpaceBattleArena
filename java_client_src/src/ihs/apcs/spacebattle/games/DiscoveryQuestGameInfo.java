package ihs.apcs.spacebattle.games;

import ihs.apcs.spacebattle.BasicGameInfo;
import ihs.apcs.spacebattle.commands.ScanCommand;

import java.util.*;

/**
 *  Discovery Quest is a game of exploration.
 *
 *  <p>Ships must 'Scan' (see {@link ScanCommand}) various objects in order to accumulate points.  Every type of object in the game is worth a different number of points.
 *  <p>Scanning is different from Radar, and requires a precise ID and takes more time and energy to perform.  It also has a limited range which you must stay within for the whole duration of the scan.
 *  <p>You CANNOT scan the same object more than once for points.
 *
 *  <p>Ships must establish an 'Outpost' by scanning it.  Once they have done so, they will start to receive 'Missions'.  They initially won't score points for scanned objects until an Outpost is established.
 *  <p>All points for things scanned before making an Outpost will be awarded when an Outpost is established.
 *
 *  <p>A Mission dictates which objects a ship should go scan.  If a ship goes and scans ONLY those things, bonus points will be awarded when they return to their outpost and Scan it again.
 *
 *  <p>Scanning their outpost will always give them a new mission.
 *
 *  <p>Your Ship being destroyed clears/fails your mission, so you must return to your established outpost if you want a new one.
 *
 *  <p>The Discovery Quest Game prevents a player from warping out of a nebula.
 * 
 * @author Michael A. Hawker
 *
 * @since 1.1
 * @version 1.1
 */
public class DiscoveryQuestGameInfo extends BasicGameInfo {
	private String[] MISSION;
	private boolean FAILED;
    private int[] CURIDS;
    private int[] SUCIDS;
		
	/**
	 * Indicates if the current missions is still a success or not.
	 * This value will be true at the start of the game.
	 * It will turn true if you scan an object that's not in your current mission.
	 * It will turn true if you are destroyed before completing your mission. 
	 * 
	 * @return true if the current mission has failed.
	 */
	public boolean isMissionFailed() { return FAILED; }
	
	/**
	 * Gets an array of strings containing the types of objects left to scan
	 *  in order to complete this mission.
	 *  
	 * <p>When this list is empty and isMissionFailed is false, your mission is complete,
	 *  you should return to your Outpost and scan it for bonus points and a new mission.
	 *  
	 * @return a list of string types
	 */
	public String[] getMissionLeft() { return MISSION; }
		
   /**
    * Gets an array of ints of ids for objects which a {@link ScanCommand} is 
    *  currently in progress for. 
    *
    * @return a list of integer ids of objects that are currently being scanned
    */
   public int[] getScanIdsInProgress() { return CURIDS; }
      
   /**
    * Gets an array of ints of ids for objects which a {@link ScanCommand} 
    *  successfully processed.
    * Will only be returned immediately after a successful scan and cleared.
    *
    * @return a list of integer ids of objects that were scanned successfully
    */
   public int[] getLastSuccessfulIds() { return SUCIDS; }
      
	@Override
	public String toString() {
		return String.format("{Mission: %s; Outpost: %s; Score: %f; Deaths: %d; High Score: %f}", Arrays.toString(getMissionLeft()), getObjectiveLocation(), getScore(), getNumDeaths(), getHighScore());
	}
}
