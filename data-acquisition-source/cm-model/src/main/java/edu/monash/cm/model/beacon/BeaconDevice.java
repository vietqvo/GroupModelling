package edu.monash.cm.model.beacon;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "macAddress", "distance", "rssi" })
public class BeaconDevice {
	
	@JsonProperty("macAddress")
	private String macAddress;
	
	@JsonProperty("distance")
	private double distance;
	
	@JsonProperty("rssi")
	private double rssi;

	public BeaconDevice() {

	}

	public BeaconDevice(String macAddress, double distance, double rssi) {
		super();
		this.macAddress = macAddress;
		this.distance = distance;
		this.rssi = rssi;
	}

	@JsonProperty("macAddress")
	public String getMacAddress() {
		return macAddress;
	}

	@JsonProperty("macAddress")
	public void setMacAddress(String macAddress) {
		this.macAddress = macAddress;
	}

	@JsonProperty("distance")
	public double getDistance() {
		return distance;
	}

	@JsonProperty("distance")
	public void setDistance(double distance) {
		this.distance = distance;
	}

	@JsonProperty("rssi")
	public double getRssi() {
		return rssi;
	}

	@JsonProperty("rssi")
	public void setRssi(double rssi) {
		this.rssi = rssi;
	}
}
