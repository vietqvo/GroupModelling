package edu.monash.cm.android.app.restservice;

import retrofit.Callback;
import retrofit.http.GET;
import retrofit.http.Query;
import edu.monash.cm.model.position.PositionData;

public interface PositionAPI {
	@GET("/api/location")
	void getCurrentLocation(@Query("btaddress") String bluetoothAddress, 
	          Callback<PositionData> callback);
}
