import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.RenderingHints;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;

class Server extends JPanel implements KeyListener, MouseListener, MouseMotionListener{
	
//THis one is better
public static DatagramSocket serverSocket;
public static InetAddress IPAddress;
public static int port;
public static int[] movements = {0,0,0,0};

	public static void createFrame(Server g) throws IOException{
	JFrame frame = new JFrame("Car GUI");
	frame.add(g);
	frame.setSize(440, 590);
	frame.setResizable(false);
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	g.addKeyListener(g);
	g.addMouseListener(g);
	g.setFocusable(true);
	frame.setVisible(true);
	}

	public static void SendSomething(String something) throws IOException{
		byte[] sendData = new byte[1024];
		sendData = something.getBytes();
		DatagramPacket sendPacket = new DatagramPacket(sendData,sendData.length, IPAddress, port);
		serverSocket.send(sendPacket);
	}
	
	public static void main(String args[]) throws Exception {
		Server demo = new Server();
		createFrame(demo);
		serverSocket = new DatagramSocket(3141);
		byte[] receiveData = new byte[1024];
		while (true) {
			demo.repaint();
			
			//System.out.println(movements[0] + " " + movements[1] + " " + movements[2] + " " + movements[3]);
			
			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			serverSocket.receive(receivePacket);
			String sentence = new String(receivePacket.getData());
			//System.out.println("RECEIVED: " + sentence);
			IPAddress = receivePacket.getAddress();
			port = receivePacket.getPort();
			//String capitalizedSentence = sentence.toUpperCase();
			//protocol:
			//forwards/backwards/right/left
			//Ex: 1011
			String msg = movements[0] + "" + movements[1] + "" + movements[2] + "" + movements[3];
			SendSomething(msg);
			}
	}

	
	public void paint(Graphics g){
		Graphics2D g2d = (Graphics2D) g;
		paintComponent(g);
		g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);
		
		//drawing background
		g2d.setColor(Color.DARK_GRAY);
		g2d.fillRect(0,0,700,700);
		
		//drawing directions
		g2d.setColor(Color.WHITE);
		g2d.drawString("Use wasd to move", 155, 400);
		g2d.drawString("   ^   ", 185, 424);
		g2d.drawString("<- | ->", 181, 430);
		g2d.drawString("   v    ", 185, 440);
		
		BufferedImage image = null;
		try {
		    URL url = new URL("http://192.168.1.11:8080/?action=snapshot&n=401");
		    image = ImageIO.read(url);
		} catch (IOException e) {
			e.printStackTrace();
		}
		g2d.drawImage(image,10,10,414,240,null);

	}
	
	
	@Override
	public void mouseDragged(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseClicked(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseReleased(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyPressed(KeyEvent arg0) {
		if(arg0.getKeyCode() == 87)
			movements[0] = 1;
		if(arg0.getKeyCode() == 83)
			movements[1] = 1;		
		if(arg0.getKeyCode() == 65)
			movements[2] = 1;	
		if(arg0.getKeyCode() == 68)
			movements[3] = 1;		
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		if(arg0.getKeyCode() == 87)
			movements[0] = 0;
		if(arg0.getKeyCode() == 83)
			movements[1] = 0;		
		if(arg0.getKeyCode() == 65)
			movements[2] = 0;	
		if(arg0.getKeyCode() == 68)
			movements[3] = 0;	
		
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}
	
	
	
	
}