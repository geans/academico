package projects.MobileSink;

import jsensor.nodes.Node;
import jsensor.nodes.models.ConnectivityModel;

public class SinkNodeConnectivity extends ConnectivityModel
{
    @Override
    public boolean isConnected(Node from, Node to) 
    {
    	if((from instanceof Sink) && (to instanceof Sensor))
    		return true;
    	else if ((from instanceof Sensor) && (to instanceof Sink))
    		return true;
    	else
    		return false;
    }
}
