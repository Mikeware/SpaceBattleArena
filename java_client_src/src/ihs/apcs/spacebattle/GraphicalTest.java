package ihs.apcs.spacebattle;

import javax.swing.*;

public class GraphicalTest implements Runnable {
	public void run() {
		JFrame frame = new JFrame("Test window");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
	
	public static void main(String[] args) {
		GraphicalTest test = new GraphicalTest();
		SwingUtilities.invokeLater(test);
	}
}
