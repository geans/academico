package projects.MobileSink;

import jsensor.nodes.Node;

public abstract class MSNode extends Node {
	public static int broadcastPackage = 0;
	public static int broadcastSignal = 1;
	public static boolean dutyCycleEnable = false;

	public static int strategy = broadcastSignal;

	public static long energyTotal;
	public static long sentTotal;
	public static long receivedTotal;

    public MSNode() {
        super();       
    }

    public static long getEnergy() {
    	return energyTotal;
    }
    
    public static long getSent() {
    	return sentTotal;
    }
    
    public static long getReceived() {
    	return receivedTotal;
    }
}
