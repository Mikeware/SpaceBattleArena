package ihs.apcs.spacebattle;

/**
 * The BasicGameInfo provides Score, HighScore, and Number of Deaths.
 * 
 * It is the basis for most other games.  It is also used for smaller 'games' which may be used to lead up to more complex ones.
 * 
 * @author Michael A. Hawker
 *
 * @since 1.0
 * @version 1.1
 */
public class BasicGameInfo {
	// Info about the player
	private double SCORE;
	private double BESTSCORE;
	private int DEATHS;
	private String LSTDSTRBY;
	
	// Info about the game
	private double HIGHSCORE;
	private double TIMELEFT;
	private double ROUNDTIME;

	/**
	 * Gets your current score.
	 * @return your current score
	 */
	public double getScore() { return SCORE; }
	
	/**
	 * Gets your current highest score for the round.
	 * @return your highest score
	 */
	public double getBestScore() { return BESTSCORE; }
	
	/**
	 * Gets the current game leader's score.
	 * @return the current game leader's score
	 */
	public double getHighScore() { return HIGHSCORE; }
	
	/**
	 * Gets the number of times you have died in this game.
	 * @return your number of deaths for this game 
	 */
	public int getNumDeaths() { return DEATHS; }
	
	/**
	 * Gets a string representing the last thing that destroyed your ship.
	 * 
	 * @return name of a player or type of an object with its #ID number
	 * @since 1.0.1
	 */
	public String getLastDestroyedBy() { return LSTDSTRBY; }
	
	/**
	 * Gets the current time remaining in the round (in seconds).
	 * @return time remaining in round in seconds
	 */
	public double getTimeRemaining() { return TIMELEFT; }
	
	/**
	 * Gets the total length of the round for this game (in seconds).
	 * <p>
	 * Will be 0 if there is currently no time limit.
	 * @return total length of time for the current game's round
	 */
	public double getTotalRoundTime() { return ROUNDTIME; } 

	@Override
	public String toString() {
		return String.format("{Score: %f; Deaths: %d; High Score: %f}", getScore(), getNumDeaths(), getHighScore());
	}
}
