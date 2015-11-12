import java.io.*;
import java.net.*;

class Server {
public static DatagramSocket serverSocket;
public static InetAddress IPAddress;
public static int port;
	public static void SendSomething(String something) throws IOException{
		byte[] sendData = new byte[1024];
		sendData = something.getBytes();
		DatagramPacket sendPacket = new DatagramPacket(sendData,sendData.length, IPAddress, port);
		serverSocket.send(sendPacket);
	}
	
	public static void main(String args[]) throws Exception {
		serverSocket = new DatagramSocket(3141);
		byte[] receiveData = new byte[1024];
		while (true) {
			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			serverSocket.receive(receivePacket);
			String sentence = new String(receivePacket.getData());
			System.out.println("RECEIVED: " + sentence);
			IPAddress = receivePacket.getAddress();
			port = receivePacket.getPort();
			//String capitalizedSentence = sentence.toUpperCase();
			}
	}
	
	
	
	
}