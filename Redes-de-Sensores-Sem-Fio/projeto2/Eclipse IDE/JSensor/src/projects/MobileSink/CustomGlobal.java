package projects.MobileSink;

import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;

import jsensor.runtime.AbsCustomGlobal;
import jsensor.runtime.Jsensor;

public class CustomGlobal extends AbsCustomGlobal{
	private long initialEnergy; 
	
	public CustomGlobal() throws IOException {
		initialEnergy = 0;
	}
	
    @Override
    public boolean hasTerminated() {
        return false;
    }
    
    @Override
    public void preRun() {
    	initialEnergy = MSNode.getEnergy();
    }

    @Override
    public void preRound() {
    }

    @Override
    public void postRound() {
    	Jsensor.log("[EnergyTotal] " + MSNode.getEnergy() + 
				" (" + 100.0 * MSNode.getEnergy() / initialEnergy + "%)");
    	Jsensor.log("[SentTotal] " + MSNode.getSent());
    	Jsensor.log("[ReceivedTotal] " + MSNode.getReceived());
    }

	@Override
	public void postRun() {
		Jsensor.log("\n\n Analysis");
    	Jsensor.log("[EnergyTotal] " + MSNode.getEnergy() + 
				" (" + 100.0 * MSNode.getEnergy() / initialEnergy + "%)");
    	Jsensor.log("[SentTotal] " + MSNode.getSent());
    	Jsensor.log("[ReceivedTotal] " + MSNode.getReceived());
    }
}
