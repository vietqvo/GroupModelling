This folder contains components:
        1. cm-android: this project is Android application to collect data from iBeacon devices via Bluetooth and other device's Bluetooth signals
        2. cm-context-service: this project is to infer indoor location from iBeacon signals and push into Redis component and then transfer data to Flume
        3. cm-ios: this project is iOS application to collect data from iBeacon devices via Bluetooth and other device's signals.
        4. cm-server: this project is to interact directly with front-end devices for indoor services, mental map inquiry
        5. cm-agent-latency: this project contains latency MR jobs to extract agent's trajectory and mental maps, and agent's physical attributes
        6. cm-disaster-latency: this project is to extract evacuation route space, hazardous functions, potential trails
        7. cm-evacuation-route: this project is to read data real-time and collected disaster latency to infer real-time evacuation route
        8. cm-simulation: this project is to read agent-latency and simulate real-time crowd dynamics
	9. cm-model: this project holds sharing pojos between above projects
