package edu.monash.cm.model.surround;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({"btAddress","detectedDevices"})
public class SurroundingDeviceDataBundle {
	

	@JsonProperty("btAddress")
	private String btAddress;

	@JsonProperty("detectedDevices")
	private List<SurroundingDevice> detectedDevices = new ArrayList<SurroundingDevice>();
	
	@JsonProperty("btAddress")
	public String getBtAddress() {
		return btAddress;
	}

	@JsonProperty("btAddress")
	public void setBtAddress(String btAddress) {
		this.btAddress = btAddress;
	}

	@JsonProperty("detectedDevices")
	public List<SurroundingDevice> getDetectedDevices() {
		return detectedDevices;
	}

	@JsonProperty("detectedDevices")
	public void setDetectedDevices(List<SurroundingDevice> detectedDevices) {
		this.detectedDevices = detectedDevices;
	}

}
