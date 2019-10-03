package projects.MobileSink;

import jsensor.nodes.messages.Message;

public class MSNodeMessage extends Message{

	public static String sendingRequest = "can i send you?";
	public static String authorizedSending = "send for me";
	private String message;
    private MSNode sender;
    private MSNode destination;
    private int hops;
    short chunk;
    
    public MSNodeMessage(MSNode sender, MSNode destination, int hops, short chunk) {
    	//Call to create a new ID
    	super(chunk);
        this.sender = sender;
        this.destination = destination;
        this.chunk = chunk;
    }

    private MSNodeMessage (MSNode sender, MSNode destination, int hops, long ID, 
    		String message) {
    	//Call to set the ID
    	this.setID(ID);
    	this.message = message;
        this.sender = sender;
        this.destination = destination;
    }

    public String getMessage(){
    	return this.message;
    }
    
    public void setMessage(String message){
    	this.message = message;
    }
    
    public MSNode getDestination() {
        return destination;
    }

    public void setDestination(MSNode destination) {
        this.destination = destination;
    }
    
    public short getChunk() {
        return chunk;
    }

    public void setChunk(short chunk) {
    	this.chunk = chunk;
    }
    
    public MSNode getSender() {
        return sender;
    }
    
    public int getHops() {
        return hops;
    }

    public void setHops(int hops) {
    	this.hops = hops;
    }

    public void setSender(MSNode sender) {
        this.sender = sender;
    }

    @Override
    public MSNodeMessage clone() {
        return new MSNodeMessage(this.getSender(), this.getDestination(),
                              this.getHops() + 1, this.getID(), this.message);
    }
}
