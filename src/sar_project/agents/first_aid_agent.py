from sar_project.agents.base_agent_gemini import SARBaseAgentGemini
# from pydantic import BaseModel, TypeAdapter
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

FIRST_AID_SYSTEM_MESSAGE="""You are a first aid specialist for search and rescue operations. Your role is to:
1. Provide detailed procedural first aid guidance and instructions
2. Advise on best medical practices"""

class FirstAidGuidanceAgent(SARBaseAgentGemini):
    def __init__(self,name):
        super().__init__(
            name=name,
            role='First Aid Specialist',
            system_message=FIRST_AID_SYSTEM_MESSAGE,
            knowledge_base=None
        )

    def get_name(self):
        """
        Returns name.
        """
        return self.name

    def get_role(self):
        """
        Returns role.
        """
        return self.role
    
    def get_system_message(self):
        """
        Returns system message used to give context to the gemini client.
        """
        return self.system_message
    
    def analyze_response(self, og_prompt: str, response: str) -> bool:
        """
        Analyzes Gemini response using a feedback loop to verify results with gemini.
        """
        analysis_context = """
        Given the prompt and response below, assess the ability of this generative AI agent
        to fulfill the goals of a first aid guidance agent that provides relevant information.
        Combine the assessment with the original JSON object response in a concise manner
        directed at the user of the first aid guidance agent using the structure:
        {
            "overall_assessment": boolean,
            "assessment_details": "complete assessment here"
            "original_response": { original JSON object response }
        }

        Prompt: """

        full_prompt = FIRST_AID_SYSTEM_MESSAGE + analysis_context + og_prompt + "\n\nResponse: " + response
        analysis = self.query_gemini(full_prompt)
        print('\n\nanalysis of response: \n' + analysis + '\n\n')

        try:
            return json.loads(analysis[8:-3])
            # return json.loads(analysis)
        except json.JSONDecodeError:
            return {
                "overall_assessment_validity": False,
                "assessment_details": "Unable to parse scene safety assessment",
                "original_response": { None }
            }

    def assess_scene_safety(self, scene_description: str) -> Dict[str, any]:
        """
        Analyzes scene description for safety concerns and hazards.
        """
        context_prompt = """
        You are a search and rescue safety expert. Analyze the following scene description 
        and provide a detailed safety assessment. Format your response as a JSON object with 
        the following structure:
        {
            "safety_status": boolean,
            "identified_hazards": ["hazard1", "hazard2", ...],
            "recommended_precautions": ["precaution1", "precaution2", ...]
        }
        
        Consider environmental hazards, structural risks, chemical/biological dangers, 
        and immediate threats to rescuer safety.
        
        Scene Description: """
        
        full_prompt = context_prompt + scene_description
        response = self.query_gemini(full_prompt)

        return self.analyze_response(full_prompt,response)
        
        try:
            # return json.loads(response[8:-3])
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "safety_status": False,
                "identified_hazards": ["Unable to parse scene safety assessment"],
                "recommended_precautions": ["Await expert assessment"]
            }

    def triage_multiple_casualties(self, victim_descriptions: List[str]) -> List[Dict[str, any]]:
        """
        Performs START triage protocol assessment on multiple casualties.
        """
        context_prompt = """
        You are an emergency medical expert. Using the START triage protocol, assess the 
        following victim description and provide triage information. Format your response 
        as a JSON object with the following structure:
        {
            "triage_level": "Red|Yellow|Green|Black",
            "key_symptoms": ["symptom1", "symptom2", ...],
            "recommended_actions": ["action1", "action2", ...],
            "priority_score": integer (1-4, 1 being highest priority)
        }
        
        Base your assessment on walking ability, respiratory rate, perfusion, and mental status.
        
        Victim Description: """
        
        triage_results = []
        for description in victim_descriptions:
            full_prompt = context_prompt + description
            response = self.query_gemini(full_prompt)
            try:
                triage_results.append(json.loads(response))
            except json.JSONDecodeError:
                triage_results.append({
                    "triage_level": "Red",
                    "key_symptoms": ["Unable to parse victim condition"],
                    "recommended_actions": ["Immediate professional medical assessment required"],
                    "priority_score": 1
                })
        
        return sorted(triage_results, key=lambda x: x['priority_score'])

    def provide_first_aid_guidance(self, injury_description: str, available_supplies: List[str]) -> Dict[str, any]:
        """
        Generates step-by-step first aid instructions based on injury and supplies.
        """
        context_prompt = f"""
        You are an emergency medical professional. Provide detailed first aid instructions 
        for the following injury, considering these available supplies: {', '.join(available_supplies)}
        
        Format your response as a JSON object with the following structure:
        {{
            "steps": ["step1", "step2", ...],
            "warnings": ["warning1", "warning2", ...],
            "required_supplies": ["supply1", "supply2", ...],
            "monitoring_instructions": "detailed monitoring instructions"
        }}
        
        Prioritize life-saving interventions and provide clear, actionable steps.
        
        Injury Description: """
        
        full_prompt = context_prompt + injury_description
        response = self.query_gemini(full_prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "steps": ["Seek immediate professional medical attention"],
                "warnings": ["Unable to parse first aid instructions"],
                "required_supplies": [],
                "monitoring_instructions": "Monitor vital signs continuously"
            }

    def monitor_vital_signs(self, vitals_data: Dict[str, float], medical_history: Optional[str] = None) -> Dict[str, any]:
        """
        Analyzes vital signs and provides monitoring guidance.
        """
        context_prompt = f"""
        You are an emergency medical professional. Analyze these vital signs and medical history 
        to provide monitoring guidance. Format your response as a JSON object with the following structure:
        {{
            "status": "stable|concerning|critical",
            "concerns": ["concern1", "concern2", ...],
            "recommended_frequency": "monitoring frequency",
            "alert_thresholds": {{
                "heart_rate": [lower_bound, upper_bound],
                "blood_pressure": [lower_bound, upper_bound],
                "respiratory_rate": [lower_bound, upper_bound],
                "oxygen_saturation": [lower_bound, upper_bound]
            }}
        }}
        
        Medical History: {medical_history if medical_history else 'Not provided'}
        Vital Signs: {json.dumps(vitals_data)}
        """
        
        response = self.query_gemini(context_prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "status": "unknown",
                "concerns": ["Unable to parse vital signs analysis"],
                "recommended_frequency": "Continuous monitoring",
                "alert_thresholds": {
                    "heart_rate": [60, 100],
                    "blood_pressure": [90, 140],
                    "respiratory_rate": [12, 20],
                    "oxygen_saturation": [95, 100]
                }
            }

    def generate_handoff_report(self, case_details: Dict[str, any], interventions: List[str]) -> str:
        """
        Creates structured handoff report for medical professionals.
        """
        context_prompt = f"""
        You are an emergency medical professional preparing a handoff report. Create a detailed 
        SBAR (Situation, Background, Assessment, Recommendation) report based on the following 
        case details and interventions. Format your response as clear text with clear section headers.

        Case Details: {json.dumps(case_details)}
        Interventions Performed: {', '.join(interventions)}
        """
        
        return self.query_gemini(context_prompt)

    def get_evacuation_guidance(self, patient_condition: str, terrain_description: str, available_resources: List[str]) -> Dict[str, any]:
        """
        Provides guidance on safe patient evacuation methods.
        """
        context_prompt = f"""
        You are a search and rescue expert. Provide evacuation guidance based on the following 
        information. Format your response as a JSON object with the following structure:
        {{
            "recommended_method": "evacuation method",
            "required_personnel": number,
            "special_considerations": ["consideration1", "consideration2", ...],
            "contraindications": ["contraindication1", "contraindication2", ...]
        }}
        
        Consider these available resources: {', '.join(available_resources)}
        Terrain Description: {terrain_description}
        
        Patient Condition: """
        
        full_prompt = context_prompt + patient_condition
        response = self.query_gemini(full_prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "recommended_method": "Await professional evacuation team",
                "required_personnel": 2,
                "special_considerations": ["Unable to parse evacuation guidance"],
                "contraindications": ["Proceed only with professional guidance"]
            }

# Example usage:
"""
agent = FirstAidGuidanceAgent('your-api-key')

# Scene safety assessment
scene_description = "Indoor collapse scenario with visible dust and debris. Smell of gas present."
safety_assessment = agent.assess_scene_safety(scene_description)

# Triage multiple casualties
victim_descriptions = [
    "Adult male, conscious but confused, bleeding from head wound",
    "Child, alert and crying, minor scrapes",
]
triage_results = agent.triage_multiple_casualties(victim_descriptions)

# First aid guidance
injury = "Compound fracture of lower leg, moderate bleeding"
supplies = ["first aid kit", "splints", "bandages", "antiseptic"]
guidance = agent.provide_first_aid_guidance(injury, supplies)
"""