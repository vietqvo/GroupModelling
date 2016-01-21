package edu.monash.cm.android.app.view;

import org.codehaus.jackson.map.ObjectMapper;

import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;

import com.mapbox.mapboxsdk.events.MapListener;
import com.mapbox.mapboxsdk.events.RotateEvent;
import com.mapbox.mapboxsdk.events.ScrollEvent;
import com.mapbox.mapboxsdk.events.ZoomEvent;
import com.mapbox.mapboxsdk.views.MapView;

import edu.monash.cm.android.R;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.map.controller.AbsMapController;
import edu.monash.cm.android.app.map.widget.MapController;
import edu.monash.cm.android.app.utils.BaseActivity;
import edu.monash.cm.model.position.PositionData;

public class MapActivity extends BaseActivity implements OnClickListener,
		MapListener {

	private MapView mMapView;
	private AbsMapController mapController;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_map);

		mMapView = (MapView) findViewById(R.id.map_mainmap);
		mMapView.addListener(this);

		mapController = new MapController(mMapView, this);
		PositionData initialPosition;
		try {
			String receivedData = getIntent().getStringExtra(
					Constants.INITIAL_POSITION);
			initialPosition = new ObjectMapper().readValue(receivedData,
					PositionData.class);

		} catch (Exception e) {
			System.out.println("Exception converting initial Position "
					+ e.getMessage());
			initialPosition = new PositionData();
		}

		mapController.displayMap(initialPosition);
	}

	@Override
	public void onResume() {
		super.onResume();
	}
	
	@Override
	public void onRotate(RotateEvent arg0) {
	}

	@Override
	public void onScroll(ScrollEvent arg0) {
	}

	@Override
	public void onZoom(ZoomEvent arg0) {
	}

	@Override
	public void onClick(View v) {
	}
}
