package edu.monash.cm.model.surround;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "bluetoothAddress", "rssi" })
public class SurroundingDevice {
	
	@JsonProperty("bluetoothAddress")
	private String bluetoothAddress;
	
	@JsonProperty("rssi")
	private String rssi;

	public SurroundingDevice(String _bluetoothAddress, String _rssi) {
		this.bluetoothAddress = _bluetoothAddress;
		this.rssi = _rssi;
	}

	@JsonProperty("bluetoothAddress")
	public String getBluetoothAddress() {
		return bluetoothAddress;
	}
	
	@JsonProperty("bluetoothAddress")
	public void setBluetoothAddress(String bluetoothAddress) {
		this.bluetoothAddress = bluetoothAddress;
	}

	@JsonProperty("rssi")
	public String getRssi() {
		return rssi;
	}

	@JsonProperty("rssi")
	public void setRssi(String rssi) {
		this.rssi = rssi;
	}

	@Override
	public boolean equals(Object object) {
		boolean isEqual = false;

		if (object != null && object instanceof SurroundingDevice) {
			isEqual = (this.bluetoothAddress == ((SurroundingDevice) object).getBluetoothAddress());
		}

		return isEqual;
	}

	@Override
	public int hashCode() {
		return this.bluetoothAddress.hashCode();
	}
}
