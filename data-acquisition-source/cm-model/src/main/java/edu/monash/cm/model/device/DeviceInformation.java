package edu.monash.cm.model.device;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "bluetoothAddress", "macAddress", "username" })
public class DeviceInformation {

	@JsonProperty("bluetoothAddress")
	private String bluetoothAddress;

	@JsonProperty("macAddress")
	private String macAddress;

	@JsonProperty("username")
	private String username;

	public DeviceInformation(String bluetoothAddress, String macAddress,
			String username) {
		super();
		this.bluetoothAddress = bluetoothAddress;
		this.macAddress = macAddress;
		this.username = username;
	}

	@JsonProperty("bluetoothAddress")
	public String getBluetoothAddress() {
		return bluetoothAddress;
	}

	@JsonProperty("bluetoothAddress")
	public void setBluetoothAddress(String bluetoothAddress) {
		this.bluetoothAddress = bluetoothAddress;
	}

	@JsonProperty("macAddress")
	public String getMacAddress() {
		return macAddress;
	}

	@JsonProperty("macAddress")
	public void setMacAddress(String macAddress) {
		this.macAddress = macAddress;
	}

	@JsonProperty("username")
	public String getUsername() {
		return username;
	}

	@JsonProperty("username")
	public void setUsername(String username) {
		this.username = username;
	}

}
