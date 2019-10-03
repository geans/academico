package projects.MobileSink;

import java.util.LinkedList;

import jsensor.nodes.messages.Inbox;
import jsensor.nodes.messages.Message;
import jsensor.runtime.Jsensor;
import jsensor.utils.Configuration;

public class Sink extends MSNode {
	public LinkedList<Long> messagesIDs;
	private LinkedList<MSNode> sensorDiscovered;
	private boolean occupied;
	private int sensorID;
	private long timeLimit;
	
	public Sink() {
		messagesIDs = new LinkedList<Long>();
		sensorDiscovered = new LinkedList<MSNode>();
		occupied = false;
		timeLimit = -1;
		sensorID = -1;
	}

    @Override
    public void handleMessages(Inbox inbox) {
    	while (inbox.hasMoreMessages()) {
    		if (timeLimit >= 0 && timeLimit < Jsensor.currentTime) {
    			timeLimit = -1;
    			sensorID = -1;
    			occupied = false;
    		}
    		
    		// TODO, check strategy
            Message msgTmp = inbox.getNextMessage();

            if (msgTmp instanceof MSNodeMessage) {
            	MSNodeMessage message = (MSNodeMessage) msgTmp;
            	String strMessage = message.getMessage();

                if (!this.messagesIDs.contains(message.getID())) {
                    this.messagesIDs.add(message.getID());
                    MSNode destNode = message.getSender();
                    // check sensor
                    if (occupied && sensorID >= 0) {
                    	if (destNode.getID() != sensorID) {
                    		Jsensor.log("[Sink Occupied] time: " + Jsensor.currentTime + 
                    				"\t sinkID: " + this.ID);
                    		continue;
                    	}
                    	else {
                    		occupied = false;
                    		sensorID = -1;
                    	}
                    }                    	
                    
                    // check strategy
                    if (strMessage == MSNodeMessage.sendingRequest) {
                    	Jsensor.log("[Received Signal Request] time: " + Jsensor.currentTime + 
                    			"\t sinkID: " + this.ID + "\t receivedFrom: " + 
                    			message.getSender().getID());
	                    
	                    MSNodeMessage msg = new MSNodeMessage((MSNode)this, destNode, 0,
	                                                    getChunk());
	                    msg.setMessage(MSNodeMessage.authorizedSending);
	                    Jsensor.log("[Sent Authorization] time: " + Jsensor.currentTime + 
                    			"\t sinkID: " + this.ID + "\t to sensorID: " + 
                    			message.getSender().getID());
	                    this.unicast(msg, destNode);
	                    occupied = true;
	                    timeLimit = Jsensor.currentTime + 1;
                    }
                    else {

	                    Jsensor.log("[Received Package] time: " + Jsensor.currentTime + 
	                    		"\t sinkID: " +
	                                this.ID + "\t receivedFrom: " + message.getSender().getID() + "\t msg: " +
	                                message.getMessage());
	                    MSNode.receivedTotal += message.getMessage().length();
                    }
                }
                if (!this.sensorDiscovered.contains(message.getSender())) {
                	this.sensorDiscovered.add(message.getSender());
                	Jsensor.log("[Discovered] time: " + Jsensor.currentTime + 
                			"\t sinkID: " +
                            	this.ID + "\t discovers new node: " + message.getSender().getID());
                }
            }
            
        }
    }

    @Override
    public void onCreation() {
    	//initializes the list of messages received by the node.
        this.messagesIDs = new LinkedList<Long>();
        
    	//probability of move
    	if(this.getRandom().nextDouble() < 0.8){
	    	SinkMobilityTimer sinkMove = new SinkMobilityTimer();
	    	sinkMove.start(this, this.getRandom().nextInt(100), Configuration.numberOfRounds, 10);	    	
    	}
    }
}
