package edu.monash.cm.model.beacon;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonPropertyOrder({ "btAddress", "detectedBeacons" })
public class BeaconDataBundle {
	
	@JsonProperty("btAddress")
	private String btAddress;
	
	@JsonProperty("detectedBeacons")
	private List<BeaconDevice> detectedBeacons = new ArrayList<BeaconDevice>();

	@JsonProperty("btAddress")
	public String getBtAddress() {
		return btAddress;
	}

	@JsonProperty("btAddress")
	public void setBtAddress(String btAddress) {
		this.btAddress = btAddress;
	}

	@JsonProperty("detectedBeacons")
	public List<BeaconDevice> getDetectedBeacons() {
		return detectedBeacons;
	}

	@JsonProperty("detectedBeacons")
	public void setDetectedBeacons(List<BeaconDevice> detectedBeacons) {
		this.detectedBeacons = detectedBeacons;
	}

}
