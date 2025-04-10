import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class JoystickDriveVisualizer extends JPanel implements MouseMotionListener {
    private int centerX = 200, centerY = 200;
    private int joyX = centerX, joyY = centerY;
    private final double L = 18.0; // Length of robot
    private final double W = 18.0; // Width of robot

    public JoystickDriveVisualizer() {
        addMouseMotionListener(this);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;

        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Draw joystick area
        g2.setColor(Color.LIGHT_GRAY);
        g2.drawOval(centerX - 100, centerY - 100, 200, 200);

        // Draw joystick position
        g2.setColor(Color.BLUE);
        g2.fillOval(joyX - 10, joyY - 10, 20, 20);

        // Compute joystick values (-1 to 1)
        double Xj = (joyX - centerX) / 100.0;
        double Yj = (joyY - centerY) / 100.0;
        Yj = Math.max(-1, Math.min(1, Yj));
        Xj = Math.max(-1, Math.min(1, Xj));

        // Equations
        double FWD = -Yj;
        double STR = -Xj * Math.signum(Yj);
        double RCW = STR * Math.sqrt(L*L + W*W) / L;

        // Display values
        g2.setColor(Color.BLACK);
        g2.drawString(String.format("Joystick X: %.2f", Xj), 20, 20);
        g2.drawString(String.format("Joystick Y: %.2f", Yj), 20, 40);
        g2.drawString(String.format("FWD = %.2f", FWD), 20, 70);
        g2.drawString(String.format("STR = %.2f", STR), 20, 90);
        g2.drawString(String.format("RCW = %.2f", RCW), 20, 110);
    }

    @Override
    public void mouseDragged(MouseEvent e) {
        joyX = e.getX();
        joyY = e.getY();
        repaint();
    }

    @Override
    public void mouseMoved(MouseEvent e) {
        // No action needed
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Joystick Drive Visualizer");
        JoystickDriveVisualizer panel = new JoystickDriveVisualizer();
        frame.add(panel);
        frame.setSize(400, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
