package edu.monash.cm.model.layout;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({ "physicalLayout", "imageMapLayout", "imageMapURL" })
public class MapModel {

	@JsonProperty("physicalLayout")
	private LayoutSize physicalLayout;
	
	@JsonProperty("imageMapLayout")
	private LayoutSize imageMapLayout;
	
	@JsonProperty("imageMapURL")
	private String imageMapURL;

	@JsonProperty("physicalLayout")
	public LayoutSize getPhysicalLayout() {
		return physicalLayout;
	}

	@JsonProperty("physicalLayout")
	public void setPhysicalLayout(LayoutSize physicalLayout) {
		this.physicalLayout = physicalLayout;
	}

	@JsonProperty("imageMapLayout")
	public LayoutSize getImageMapLayout() {
		return imageMapLayout;
	}

	@JsonProperty("imageMapLayout")
	public void setImageMapLayout(LayoutSize imageMapLayout) {
		this.imageMapLayout = imageMapLayout;
	}

	@JsonProperty("imageMapURL")
	public String getImageMapURL() {
		return imageMapURL;
	}

	@JsonProperty("imageMapURL")
	public void setImageMapURL(String imageMapURL) {
		this.imageMapURL = imageMapURL;
	}
	
	
}
