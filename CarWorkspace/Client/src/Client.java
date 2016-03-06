import java.net.* ;

public class Client
{
   private final static int PACKETSIZE = 1024;

   
   public static void main( String args[] )
   {

      DatagramSocket socket = null ;

      while(true){
      try
      {
         InetAddress host = InetAddress.getByName("10.170.67.252") ;
         int port         = 3141;

         socket = new DatagramSocket() ;

         byte [] data = "Test".getBytes();
         DatagramPacket packet = new DatagramPacket( data, data.length, host, port ) ;

         socket.send( packet ) ;

         Thread.sleep(1000);
      }
      catch( Exception e )
      {
         System.out.println( e ) ;
      }
      finally
      {
         if( socket != null )
            socket.close() ;
      }
   }
}
}