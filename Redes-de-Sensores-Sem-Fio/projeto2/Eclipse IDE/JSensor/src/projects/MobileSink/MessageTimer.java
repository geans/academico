package projects.MobileSink;

import jsensor.nodes.events.TimerEvent;

import jsensor.nodes.Node;
import jsensor.runtime.Jsensor;

public class MessageTimer extends TimerEvent {
	
	public MessageTimer() {
		this.setFireTime(0.001);
	}
	
    @Override
    public void fire() {
        if ( ! (this.node instanceof Sensor) ) // only sensors generates messages
        	return;
        if (MSNode.dutyCycleEnable &&
        		! ((Sensor) this.node).inWorkCycle()) { // sensor sleeping
        	Jsensor.log("[Sleeping] nodeId: " + this.node.getID());
			return;
        }
        
        String strMessage = "";
        MSNode destSink = (MSNode) Jsensor.getNodeByID(((Sensor) this.node).getSink());
        MSNodeMessage msg = new MSNodeMessage((MSNode)this.node, destSink, 0,
                                        this.node.getChunk());
	    
	    if (MSNode.strategy == MSNode.broadcastPackage) {
	        strMessage = "This is the message number " + this.node.getChunk() +
	                " created by the node " + node.getID();
	        msg.setMessage(strMessage);
	        Jsensor.log("[Sent Package] time: " + Jsensor.currentTime + 
	        		" nodeID: " + this.node.getID());

		    if ( ! ((Sensor) this.node).radioOn(strMessage.length()) ) // check energy of sensor
	        	return;
		    
	        this.node.multicast(msg);
	    }
	    else if (MSNode.strategy == MSNode.broadcastSignal) {
	        strMessage = MSNodeMessage.sendingRequest;
	        msg.setMessage(strMessage);
	        Jsensor.log("[Event] time: " + Jsensor.currentTime + 
	        		" nodeID: " + this.node.getID());

		    if ( ! ((Sensor) this.node).radioOn(strMessage.length()) ) // check energy of sensor
	        	return;
		    
	        this.node.multicast(msg);
	        ((Sensor)this.node).signalEnable = true;
	    }
        
        MSNode.sentTotal += strMessage.length();
        MSNode.energyTotal -= strMessage.length();
    }
}
