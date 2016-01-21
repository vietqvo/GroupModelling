package edu.monash.cm.android.app.map.widget;

import android.content.Context;
import android.graphics.Canvas;
import android.os.Handler;
import android.util.AttributeSet;

import com.mapbox.mapboxsdk.tileprovider.MapTileLayerBase;
import com.mapbox.mapboxsdk.views.MapView;

public class MyMapView extends MapView {

	public MyMapView(Context context) {
		super(context);
	}

	public MyMapView(Context context, AttributeSet attrs) {
		super(context, attrs);
	}

	public MyMapView(Context context, int tileSizePixels,
			MapTileLayerBase aTileProvider) {
		super(context, tileSizePixels, aTileProvider);

	}

	public MyMapView(Context arg0, int arg1, MapTileLayerBase arg2,
			Handler arg3, AttributeSet arg4) {
		super(arg0, arg1, arg2, arg3, arg4);
	}

	@Override
	protected void onDraw(Canvas c) {
		super.onDraw(c);
	}
}
