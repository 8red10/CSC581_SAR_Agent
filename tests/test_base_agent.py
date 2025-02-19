from sar_project.agents.base_agent_gemini import SARBaseAgentGemini

def main():
    print('Starting test...')
    g = SARBaseAgentGemini(name='greg',role='test agent',system_message='')
    response = g.test_prompt('hi there')
    print(response)

if __name__ == '__main__':
    main()
