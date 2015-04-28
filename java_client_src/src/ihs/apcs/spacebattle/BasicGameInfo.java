package ihs.apcs.spacebattle;

/**
 * The BasicGameInfo provides Score, HighScore, and Number of Deaths.
 * 
 * It is the basis for most other games.  It is also used for smaller 'games' which may be used to lead up to more complex ones.
 * 
 * @author Michael A. Hawker
 *
 * @since 2.0
 * @version 1.0
 */
public class BasicGameInfo {
	private double SCORE;
	private double HIGHSCORE;
	private int DEATHS;

	/**
	 * Gets your current score.
	 * @return your current score
	 */
	public double getScore() { return SCORE; }
	
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

	@Override
	public String toString() {
		return String.format("{Score: %f; Deaths: %d; High Score: %f}", getScore(), getNumDeaths(), getHighScore());
	}
}
