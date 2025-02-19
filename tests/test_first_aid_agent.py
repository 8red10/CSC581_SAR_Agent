import pytest
from unittest.mock import Mock, patch
from sar_project.agents.first_aid_agent import FirstAidGuidanceAgent
import json

# Mock responses for different scenarios
MOCK_SCENE_SAFETY_RESPONSE = {
    "safety_status": False,
    "identified_hazards": ["Gas leak", "Structural instability"],
    "recommended_precautions": ["Wear PPE", "Evacuate area"]
}

MOCK_TRIAGE_RESPONSE = {
    "triage_level": "Red",
    "key_symptoms": ["Severe bleeding", "Altered consciousness"],
    "recommended_actions": ["Apply direct pressure", "Monitor vital signs"],
    "priority_score": 1
}

MOCK_FIRST_AID_RESPONSE = {
    "steps": ["Apply pressure", "Elevate limb"],
    "warnings": ["Do not remove embedded objects"],
    "required_supplies": ["Gauze", "Bandages"],
    "monitoring_instructions": "Check bleeding every 5 minutes"
}

MOCK_VITALS_RESPONSE = {
    "status": "stable",
    "concerns": ["Slightly elevated heart rate"],
    "recommended_frequency": "Every 15 minutes",
    "alert_thresholds": {
        "heart_rate": [60, 100],
        "blood_pressure": [90, 140],
        "respiratory_rate": [12, 20],
        "oxygen_saturation": [95, 100]
    }
}

MOCK_HANDOFF_RESPONSE = """
SITUATION:
Patient found in collapsed structure
BACKGROUND:
No known medical history
ASSESSMENT:
Multiple trauma, stable vital signs
RECOMMENDATION:
Transfer to trauma center
"""

MOCK_EVACUATION_RESPONSE = {
    "recommended_method": "Stretcher evacuation",
    "required_personnel": 4,
    "special_considerations": ["C-spine precautions"],
    "contraindications": ["Rapid movement"]
}

@pytest.fixture
def mock_agent():
    """Create a mock agent with simulated Gemini API responses"""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        # Configure the mock to return different responses for different prompts
        mock_response = Mock()
        mock_response.text = json.dumps(MOCK_SCENE_SAFETY_RESPONSE)
        mock_model.return_value.generate_content.return_value = mock_response
        
        agent = FirstAidGuidanceAgent('dummy agent')
        return agent

class TestFirstAidGuidanceAgent:
    def test_assess_scene_safety_valid_input(self, mock_agent):
        """Test scene safety assessment with valid input"""
        scene_description = "Building collapse with visible gas leak"
        result = mock_agent.assess_scene_safety(scene_description)
        
        assert isinstance(result, dict)
        assert "safety_status" in result
        assert "identified_hazards" in result
        assert "recommended_precautions" in result
        assert len(result["identified_hazards"]) > 0

    def test_triage_multiple_casualties_valid_input(self, mock_agent):
        """Test triage function with valid input"""
        victim_descriptions = [
            "Adult male, unconscious, breathing",
            "Child, alert and oriented"
        ]
        
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = json.dumps(MOCK_TRIAGE_RESPONSE)
            mock_generate.return_value = mock_response
            
            result = mock_agent.triage_multiple_casualties(victim_descriptions)
            
            assert isinstance(result, list)
            assert len(result) == len(victim_descriptions)
            assert all("triage_level" in r for r in result)
            assert all("priority_score" in r for r in result)

    def test_provide_first_aid_guidance_valid_input(self, mock_agent):
        """Test first aid guidance with valid input"""
        injury_description = "Compound fracture of lower leg"
        available_supplies = ["first aid kit", "splints", "bandages"]
        
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = json.dumps(MOCK_FIRST_AID_RESPONSE)
            mock_generate.return_value = mock_response
            
            result = mock_agent.provide_first_aid_guidance(injury_description, available_supplies)
            
            assert isinstance(result, dict)
            assert "steps" in result
            assert "warnings" in result
            assert "required_supplies" in result
            assert len(result["steps"]) > 0

    def test_monitor_vital_signs_valid_input(self, mock_agent):
        """Test vital signs monitoring with valid input"""
        vitals_data = {
            "heart_rate": 80,
            "blood_pressure": 120,
            "respiratory_rate": 16,
            "oxygen_saturation": 98
        }
        
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = json.dumps(MOCK_VITALS_RESPONSE)
            mock_generate.return_value = mock_response
            
            result = mock_agent.monitor_vital_signs(vitals_data)
            
            assert isinstance(result, dict)
            assert "status" in result
            assert "concerns" in result
            assert "alert_thresholds" in result

    def test_generate_handoff_report_valid_input(self, mock_agent):
        """Test handoff report generation with valid input"""
        case_details = {
            "patient_age": 45,
            "mechanism_of_injury": "Fall from height",
            "vital_signs": {"bp": "120/80", "hr": 85}
        }
        interventions = ["C-collar applied", "IV access obtained"]
        
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = MOCK_HANDOFF_RESPONSE
            mock_generate.return_value = mock_response
            
            result = mock_agent.generate_handoff_report(case_details, interventions)
            
            assert isinstance(result, str)
            assert "SITUATION" in result
            assert "BACKGROUND" in result
            assert "ASSESSMENT" in result
            assert "RECOMMENDATION" in result

    def test_get_evacuation_guidance_valid_input(self, mock_agent):
        """Test evacuation guidance with valid input"""
        patient_condition = "Suspected spinal injury"
        terrain_description = "Steep, rocky terrain"
        available_resources = ["Stretcher", "Neck collar", "Ropes"]
        
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = json.dumps(MOCK_EVACUATION_RESPONSE)
            mock_generate.return_value = mock_response
            
            result = mock_agent.get_evacuation_guidance(
                patient_condition, 
                terrain_description, 
                available_resources
            )
            
            assert isinstance(result, dict)
            assert "recommended_method" in result
            assert "required_personnel" in result
            assert "special_considerations" in result

    def test_error_handling(self, mock_agent):
        """Test error handling with invalid API responses"""
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = "Invalid JSON"
            mock_generate.return_value = mock_response
            
            # Test each function's error handling
            scene_result = mock_agent.assess_scene_safety("Test scene")
            assert isinstance(scene_result, dict)
            assert "safety_status" in scene_result
            
            triage_result = mock_agent.triage_multiple_casualties(["Test victim"])
            assert isinstance(triage_result, list)
            assert len(triage_result) > 0
            
            guidance_result = mock_agent.provide_first_aid_guidance("Test injury", [])
            assert isinstance(guidance_result, dict)
            assert "steps" in guidance_result

    @pytest.mark.parametrize("vitals_data", [
        {"heart_rate": 180},  # Abnormally high
        {"heart_rate": 40},   # Abnormally low
        {},                   # Empty
    ])
    def test_vital_signs_edge_cases(self, mock_agent, vitals_data):
        """Test vital signs monitoring with edge cases"""
        with patch.object(mock_agent.model, 'generate_content') as mock_generate:
            mock_response = Mock()
            mock_response.text = json.dumps(MOCK_VITALS_RESPONSE)
            mock_generate.return_value = mock_response
            
            result = mock_agent.monitor_vital_signs(vitals_data)
            assert isinstance(result, dict)
            assert "status" in result
            assert "alert_thresholds" in result

if __name__ == "__main__":
    pytest.main([__file__])