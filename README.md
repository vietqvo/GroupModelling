##### REAL-TIME DATA ACQUISITION FOR CROWD MODELLING
---
This project aims at collecting data for crowd simulation model enhancement and disaster prevention.

Contributors: 

1. [**Viet Quang Vo**](mailto:viet.vo@monash.edu) -Student

2. [**Bernd Meyer**](http://berndmeyer.net/) -Supervisor

3. [**Aldeida Aleti**](http://users.monash.edu.au/~aldeidaa/) -Supervisor

This is the NICTA collaborative project between the faculties of IT, Engineering and Social Science at Monash University. It aims at collecting data for crowd dynamics simulation enhancement and disaster prevention at before and during disasters happens bby eexploring various optimisation techniques for an adaptive cost function. It comprises following folders:

1.documents: This folder contains 'in-progress' papers, thesis, and relevant reference documents 

2.data-acquisition-source: This folder contains components:

        2.1 cm-android: this project is Android application to collect data from iBeacon devices via BlueTooth and other device's BlueTooth signals.
        
        2.2 cm-context-service: this project is to infer indoor location from iBeacon signals and push into Redis component and then transfer data to Flume.
        
        2.3 cm-ios: this project is iOS application to collect data from iBeacon devices via BlueTooth and other device's signals.
        
        2.4 cm-server: this project is to interact directly with front-end devices for indoor services, mental map inquiry
        
        2.5 cm-agent-latency: this project contains latency MR jobs to extract agent's trajectory and mental maps, and agent's physical attributes.
        
        2.6 cm-disaster-latency: this project is to extract evacuation route space, hazardous functions, potential trails, response functions.
        
        2.7 cm-evacuation-route: this project is to read data real-time and collected disaster latency to infer real-time evacuation route.
        
        2.8 cm-simulation: this project is to read agent-latency and simulate real-time crowd dynamics.
        
        2.8 cm-model: this project holds sharing POJOs between above projects.

3.crowd-simulation-source: This project is for simulating crowd dynamics on micro and micro flows

4.analysis: this folder is for data explaination, result representation analysis  
        
5.misc

