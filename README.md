# Audi MH2P MMI/HMI DOS Attack and CAN Bus Analysis

This repository contains a CAN-Bus Analysis and of a Denial of Service (DOS) attack executed on the Audi MH2P MMI/HMI system. The attack utilizes Touch packets to disrupt system functionality. In addition, the repository provides system data extracted from the ECU, along with multiple visualizations for the CAN Dumps.

## Project Overview

### Attack Methodology
- **DOS Attack:** Leveraging Touch packets to overwhelm the MH2P MMI/HMI system.
- **CAN BUS Dumper:**
  - **Transition Aggregation Vector**
  - **Dump extraction in CSV Files**
  - **Frequency Analysis**
  - **Bitflip Analysis**
  - **Monotonic Analysis**

### Data Extraction
The ECU (Electronic Control Unit) data has been extracted from temporary Files which contain information such as temperature, frequency and voltage for side channel analysis.

- **Raw ECU Data:** Directly extracted data from the Audi MH2P ECU.
- **Processed CAN Data:** Dumped from the 6 CAN Ports on the System.

### Visualizations of the CAN Channels

- **Frequency Charts:** Shows the occurrence frequency of specific events during the attack.
- **Bitflip Analysis:** Highlights the points of vulnerability by analyzing bit transitions.
- **Monotonic Analysis:** Visualizes the consistency and progression of the attack over time.
- **heatmaps:** Several Heatmaps of the Analysis with color coding.

cheers
