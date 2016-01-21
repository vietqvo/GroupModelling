package edu.monash.cm.android.app.map.controller;

import android.content.Context;
import android.view.View;
import edu.monash.cm.model.position.PositionData;

public abstract class AbsMapController {
	protected View mapView;
	protected Context context;

	public abstract void updateCurrentLocation(PositionData data);

	public abstract void clearCurrentLocation();

	public abstract void displayMap(PositionData initialData);

	public abstract void setMapViewCenter(PositionData center);
	
	public AbsMapController(View _mapView, Context _context) {
		mapView = _mapView;
		context = _context;
	}

	public View getMapView() {
		return mapView;
	}

	public void setMapView(View mapView) {
		this.mapView = mapView;
	}

	public Context getContext() {
		return context;
	}

	public void setContext(Context context) {
		this.context = context;
	}

}
