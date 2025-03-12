# First Aid Guidance Agent - Search and Rescue

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
- Google Gemini API Key (obtain at https://aistudio.google.com/apikey)

### Setup

1. Clone Riley's GitHub repository:

```
git clone https://github.com/rcfroomin/sar_project
cd sar-project
```

2. Set up Python environment:

```
# Using pyenv (recommended)
pyenv install 3.10.8  # or your preferred version
pyenv local 3.10.8

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
pip install -e .
```

4. Configure environment variables:

```
echo '.env.' >> .gitignore
echo 'GOOGLE_API_KEY=<your google gemini API key>' >> .env
```

Make sure to keep your `.env` file private and never commit it to version control.

5. Setup Google Gemini:

```
# via command line
pip install google-generativeai
# in the agent's python file
from google import generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
```

Utilize the `base_agent_gemini.py` file in `sar_project/src/sar_project/agents/` to help setup your agent.


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


## Feedback and Modifications

### Insights

After reviewing the feedback from my initial version of this First Aid Guidance agent, I learned that it would be valuable to incorporate a validation mechanism to ensure the Gemini responses are accurate and useful in a real-world scenario. The person giving feedback suggested utilizing a verified medical knowledge base or feedback loop to check generated responses against verified medical guidelines. As I initially inteded to have a reliable agent that would be useful in a wide variety of scenarios, validation mechanisms such as these would help improve the robustness of this agent. 


### Modifications

As a result of the feedback I received, I incorporated a feedback loop for the first aid guidance agent to check its responses. For each of the agent's functions, the agent first prompts Gemini to get an initial response, then re-prompts Gemini with the initial response and additional context to assess the validity of the initial response. The response along with its assessment is then passed to the user in a JSON object structure. This enables the agent to not only revise its initial response but also give insight to the user on the validity of the response. This provides increased reliability of the responses as the user can read how the initial response was assessed before either moving forward or prompting the agent again.


## Issues

At this initial stage of the First Aid Guidance Agent, the implementation is not perfect. Due to the variability of the result from Gemini, the python json library is not always able to decode the response and triggers the error case for the agent's function. Future work includes a more in-depth outline of the desired structure of the response from Gemini. The current implementation expects a leading \```json and a trailing \``` so it extracts the JSON object via ```json.loads(response[8:-3])```.


## Important Notice

This tool is designed to assist trained professionals and should not be used as a replacement for professional medical judgment. Always defer to trained medical professionals and established protocols in emergency situations.
