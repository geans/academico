package projects.MobileSink;

import java.util.LinkedList;
import java.util.Random;

import jsensor.runtime.Jsensor;
import jsensor.utils.Configuration;
import jsensor.nodes.messages.Inbox;
import jsensor.nodes.messages.Message;

public class Sensor extends MSNode {
	public LinkedList<Long> messagesIDs;
	private static int dutyCycle = 16; // value is exponential of 2 only
	private int mySinkID;
	private long energy;
	private boolean on;
	private int workCycle;
	protected boolean signalEnable;
	
	public Sensor() {
		energy = 100;
		on = true;
	    energyTotal += energy;
	    Random rand = new Random();
	    
	    workCycle = rand.nextInt(dutyCycle);
	    signalEnable = false;
	}

    @Override
    public void handleMessages(Inbox inbox) {
    	// No receiver message, only send to sink

    	while (inbox.hasMoreMessages()) {
    		
            Message msgTmp = inbox.getNextMessage();
            String strMessage = "This is the message number " + getChunk() +
	                " created by the node " + getID();

            if (msgTmp instanceof MSNodeMessage) {
            	
            	MSNodeMessage message = (MSNodeMessage) msgTmp;

                if (!this.messagesIDs.contains(message.getID())) {
                
                	this.messagesIDs.add(message.getID());
                    
                	if (message.getMessage() == MSNodeMessage.authorizedSending) {
                		signalEnable = false;
                		
	                    MSNode destSink = message.getSender();
	                    
	                    MSNodeMessage msg = new MSNodeMessage((MSNode)this, destSink, 0,
	                                                    getChunk());
	
	                    msg.setMessage(strMessage);
	                    Jsensor.log("[Sent] time: " + Jsensor.currentTime + " nodeID: " + getID() +
	                                " sendTo sink: " + destSink.getID());
	                    this.unicast(msg, destSink); // TODO, check less energy before
	                    MSNode.sentTotal += strMessage.length();
	                    MSNode.energyTotal -= strMessage.length();
                    }
                }
            }
        }
    }

    @Override
    public void onCreation() {
    	//initializes the list of messages received by the node.
        messagesIDs = new LinkedList<Long>();
        mySinkID = -1;
        //probability of send a message
    	if(this.getRandom().nextDouble() < 0.99){
			int time = 1 + this.getRandom().nextInt((int)Configuration.numberOfRounds);    	    
	    	MessageTimer st = new MessageTimer();
	    	st.startRelative(time, this);
    	}
    }
    
    public int findSink() {
		mySinkID = -1;
		for (Object neighbour : this.getNeighbours().getNodesList().toArray())
        	if (neighbour instanceof Sink) {
        		mySinkID = ((MSNode) neighbour).getID();
        		break;
        	}
    	return mySinkID;
    }
    
    public int getSink() {
    	return mySinkID;
    }
    
    public boolean radioOn(int time) {
    	if ( ! this.on) return false;
    	
    	boolean signal = false;
    	--energy;
    	
    	if (time <= 0)
    		time = 1;
    	
    	else if (time <= energy) {
    		energy -= time;
    		energyTotal -= time;
    		signal = true;
    	}
    	else {
    		energyTotal -= energy;
    		energy = 0;
    		on = false;
    		Jsensor.log("[Dead] nodeID: " + this.ID);
    	}
    	return signal;
    }
    
    public boolean inWorkCycle() {
    	return (Jsensor.currentTime & dutyCycle) == workCycle;
    }

}
