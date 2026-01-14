import os
from crewai import Agent, Task, Crew

# 1. Define the Sorter
sorter = Agent(
    role = 'Inbound Specialist',
    goal = 'Accurately categorize incoming requests into Sales, Support, or Junk.',
    backstory = 'You are an expert at reading between the lines and knowing what a customer truly needs.',
    allow_delegation = False,
    verbose = True
)

# 2. Define the Responder
responder = Agent(
    role = 'Communications Lead',
    goal = 'Draft a perfect, professional response based on catagory.',
    backstory = 'You are a master of tone. You are persuasive for Sales and empathetic for Support.',
    allow_delegation = False,
    verbose = True
)

# 3. Task 1: Categorization
task_classify = Task(
    description = 'Analyse the request: "{request_text}"',
    expected_output='One word: Sales, Support, or Junk.',
    agent = sorter
)

# 4. Task 2: Drafting and Saving to File
task_draft = Task(
    description='Draft a response. If junk, ignore, If sales, draft a pitch. If Support, draft a help guide. ',
    expected_output='A full email response in Markdown format.',
    agent = responder,
    context = [task_classify],
    output_file = 'latest_response.md'
)

# 5. The Crew
op_crew = Crew(
    agents = [sorter, responder],
    tasks=[task_classify, task_draft]
)

# 6. Execute with a "Messy" Input
test_request = "It's broken"
op_crew.kickoff(inputs={'request_text': test_request})