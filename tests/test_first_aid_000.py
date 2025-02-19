from sar_project.agents.first_aid_agent import FirstAidGuidanceAgent

def test000():
    agent = FirstAidGuidanceAgent('dummy agent')
    print(agent.assess_scene_safety('radioactive building with burning cows'))

def test001():
    agent = FirstAidGuidanceAgent('dummy agent')

    scene_description = "radioactive building with burning cows"
    context_prompt = """
    You are a search and rescue safety expert. Analyze the following scene description 
    and provide a detailed safety assessment. Format your response as a JSON object with 
    the following structure:
    {
        "safety_status": boolean,
        "identified_hazards": ["hazard1", "hazard2", ...],
        "recommended_precautions": ["precaution1", "precaution2", ...]
    }
    Do not include the json identifiers in the response. Only include pure json that can be parsed by the json python library.

    Consider environmental hazards, structural risks, chemical/biological dangers, 
    and immediate threats to rescuer safety.
    
    Scene Description: """
    
    full_prompt = context_prompt + scene_description
    response = agent.query_gemini(full_prompt)
    print(response[8:-3],end='\n\n')
    print(response,end='\n\n')
    

def main():
    test000()
    print()
    test001()

if __name__ == "__main__":
    main()