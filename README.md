# First Aid Guidance Agent - Search and Rescue Applications

## Author

by Jack Krammer on March 11, 2025 for Cal Poly CSC 581


## Introduction

An intelligent First Aid Guidance Agent to support the Cal Poly AI4S&R (AI for search and rescue) project. Designed to provide reliable JSON structured first aid and emergency response information using Google's Gemini API. 

The basis of this project is built upon Riley Froomin's GitHub repository (https://github.com/rcfroomin/sar_project). More details and instructions for creating your own SAR agent are included in the linked repository. 


## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pyenv (recommended for python version management)
- pip (for dependency management)

### Setup

1. Clone Riley's GitHub repository:

```
git clone https://github.com/rcfroomin/sar_project
cd sar-project
```

2. Set up Python environment:

asdfasdfs




## Agent Functionality

#### 1. Scene Safety Assessment

- Analyzes scene descriptions for potential hazards
- Provides structured safety recommendations
- Identifies environmental and situational risks
- Generates clear safety precautions

#### 2. Multiple Casualty Triage

- Implements START (Simple Triage and Rapid Treatment) protocol
- Prioritizes casualties based on severity
- Provides structured triage levels (Red/Yellow/Green/Black)
- Generates specific action recommendations

#### 3. First Aid Guidance

- Step-by-step first aid instructions
- Resource-aware recommendations based on available supplies
- Clear warnings and contraindications
- Monitoring guidelines

#### 4. Vital Signs Monitoring

- Analyzes vital sign data
- Provides monitoring frequency recommendations
- Defines alert thresholds
- Considers medical history when available

#### 5. Medical Handoff Reports

- Generates structured SBAR reports
- Ensures critical information transfer
- Includes relevant intervention history
- Provides clear recommendations

#### 6. Evacuation Guidance

- Terrain-aware evacuation recommendations
- Resource requirement specifications
- Special considerations for patient conditions
- Clear contraindications


## Issues

At this initial stage of the First Aid Guidance Agent, the implementation is not perfect. Due to the variability of the result from Gemini, the python json library is not always able to decode the response and triggers the error case for the agent's function. Future work includes a more in-depth outline of the desired structure of the response from Gemini.


## Important Notice

This tool is designed to assist trained professionals and should not be used as a replacement for professional medical judgment. Always defer to trained medical professionals and established protocols in emergency situations.
