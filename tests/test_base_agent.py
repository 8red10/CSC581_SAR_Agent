from sar_project.agents.base_agent import SARBaseAgent
from sar_project.agents.base_agent_gemini import SARBaseAgentGemini

def main():
    print('Hi')
    s = SARBaseAgent('agent000','test agent', 'system message?')
    print(s.get_config_list())
    print()

    response = s.query_gemini('hi')
    print(response)
    print('\n\n')

    g = SARBaseAgentGemini(name='greg',role='test agent')
    response = g.test_prompt('what is AI?')
    print(response)

    print('test where this line is output')

if __name__ == '__main__':
    main()
