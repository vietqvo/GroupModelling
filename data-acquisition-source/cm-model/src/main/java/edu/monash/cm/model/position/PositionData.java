package edu.monash.cm.model.position;

import org.codehaus.jackson.map.ObjectMapper;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "longitude", "latitude" })
public class PositionData {

	@JsonProperty("longitude")
	private float longitude;

	@JsonProperty("latitude")
	private float latitude;

	@JsonProperty("longitude")
	public float getLongitude() {
		return longitude;
	}

	@JsonProperty("longitude")
	public void setLongitude(float longitude) {
		this.longitude = longitude;
	}

	@JsonProperty("latitude")
	public float getLatitude() {
		return latitude;
	}

	@JsonProperty("latitude")
	public void setLatitude(float latitude) {
		this.latitude = latitude;
	}

	@Override
	public String toString() {

		ObjectMapper mapper = new ObjectMapper(); // for testing
		try {
			return mapper.writeValueAsString(this);
		} catch (Exception ex) {
			return null;
		}

	}
}
