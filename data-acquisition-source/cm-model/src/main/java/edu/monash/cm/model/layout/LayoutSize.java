package edu.monash.cm.model.layout;

import org.codehaus.jackson.map.ObjectMapper;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "width", "length" })
public class LayoutSize {

	@JsonProperty("width")
	private float width;

	@JsonProperty("length")
	private float length;

	@JsonProperty("width")
	public float getWidth() {
		return width;
	}

	@JsonProperty("width")
	public void setWidth(float width) {
		this.width = width;
	}

	@JsonProperty("length")
	public float getLength() {
		return length;
	}

	@JsonProperty("length")
	public void setLength(float length) {
		this.length = length;
	}

	@Override
	public String toString(){
		ObjectMapper mapper = new ObjectMapper(); // for testing
		try {
			return mapper.writeValueAsString(this);
		} catch (Exception ex) {
			return null;
		}
	}
}
