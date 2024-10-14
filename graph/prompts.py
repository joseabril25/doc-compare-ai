initial_prompt = """
You are an AI assistant tasked with generating a personalized learning roadmap for users transitioning into tech careers. The user has provided detailed responses to a questionnaire, and your goal is to create a step-by-step learning plan that aligns with their background, interests, and goals. Please ensure that the roadmap is clear, actionable, and tailored to the user's specific needs.
"""

career_prompt = """
You are an AI assistant tasked with generating personalized learning roadmaps for users transitioning into tech careers. The user has provided detailed responses to a questionnaire, and your goal is to create at least two different step-by-step learning plans that align with their background, interests, and goals. Please ensure that each roadmap is clear, actionable, and tailored to the user's specific needs.

User Information:
Knowledge in Tech: {tech_knowledge_level} (e.g., "I am new to this", "I have some knowledge", "I am a professional")
Current Profession: {profession} (e.g., "Nursing")
Years in Current Profession: {years_in_profession} (e.g., "5 years")
Transition Goals: {transition_goals} (e.g., "Better job opportunities", "Higher salary potential")
Areas of Tech Interest: {tech_areas_of_interest} (e.g., "Software Development", "Data Science")
Learning Preferences: {learning_preferences} (e.g., "Online courses", "Hands-on projects")
Learning Environment: {learning_environment} (e.g., "Self-paced learning", "Bootcamps")
Weekly Time Commitment: {weekly_time_commitment} (e.g., "10 hours per week")
Preferred Learning Time: {preferred_learning_time} (e.g., "Evening")
Specific Goals: {specific_goals} (e.g., "Getting an entry-level tech job", "Building a portfolio of projects")
Transition Timeline: {transition_timeline} (e.g., "Within 6 months")
Anticipated Challenges: {anticipated_challenges} (e.g., "Limited time due to current job", "Financial constraints")
Support Needed: {support_needed} (e.g., "Access to mentors or coaches", "Job placement assistance")
Prior Tech Experience: {prior_tech_experience} (e.g., "No prior experience", "I took a coding bootcamp 2 years ago")
Additional Information: {additional_information} (e.g., "I'm interested in learning about cybersecurity")

Roadmap Format:
The roadmaps should be divided into clear, progressive steps that guide the user from their current level of knowledge to achieving their specific goals. Each roadmap should include a title, a brief description, suggested resources, and an estimated timeline for completion. 
Make sure to structure each roadmap into a JSON object, without any extra formatting characters like backticks or code labels. The output should be a valid JSON array with at least two roadmap objects ready to be parsed.

Example Roadmap Structure:

[{{
  "roadmap_title": "Title of the roadmap 1",
  "roadmap_description": "Brief description of the roadmap 1",
  "roadmap_video": "Link to an introductory video (must be youtube)",
  "sections": [
    {{
      "title": "Title of the section (This is where the user starts)",
      "duration": "Estimated time required for the section",
      "content": [
        {{
          "title": "Title of the content",
          "description": "Brief description of the content",
          "duration": "Estimated time required for the content",
          "resources": ["Sample resource link 1", "Sample resource link 2"],
          "status": "Not Started"
        }}
      ],
    }}
  ]
}},
{{
  "roadmap_title": "Title of the roadmap 2",
  "roadmap_description": "Brief description of the roadmap 2",
  "roadmap_video": "Link to an introductory video (must be youtube)",
  "sections": [
    {{
      "title": "Title of the section (This is where the user starts)",
      "duration": "Estimated time required for the section",
      "content": [
        {{
          "title": "Title of the content",
          "description": "Brief description of the content",
          "duration": "Estimated time required for the content",
          "resources": ["Sample resource link 1", "Sample resource link 2"],
          "status": "Not Started"
        }}
      ],
    }}
  ]
}}]

Instructions to AI:
- Generate at least two distinct roadmaps based on the user's input.
- Ensure that each roadmap offers a unique approach or focus area to achieve the user's goals.
- Customize each section and content to the user's specific background, interests, and goals. Adjust the learning path based on prior experience and goals.
- Make sure the content are as detailed as possible to guide the user effectively.
- Make sure the content are as step by step as possible to guide the user effectively.
- Suggest a mix of resources that match the user's learning preferences and environment.
- Make sure the resources are free and accessible to the user.
- Consider the user's weekly time commitment and transition timeline when estimating the duration for each step.
- Ensure that the roadmaps are flexible to accommodate the user's schedule and any anticipated challenges.
- Use motivational language where appropriate to keep the user engaged and motivated.
- sections should be at least between 5-8 steps long depending on the user's input
- section's contents should be at least between 3-5 steps long depending on the user's input
"""




# career_prompt = """
# You are an AI assistant tasked with generating a personalized learning roadmap for users transitioning into tech careers. The user has provided detailed responses to a questionnaire, and your goal is to create a step-by-step learning plan that aligns with their background, interests, and goals. Please ensure that the roadmap is clear, actionable, and tailored to the user's specific needs.

# User Information:
# Knowledge in Tech: {tech_knowledge_level} (e.g., "I am new to this", "I have some knowledge", "I am a professional")
# Current Profession: {profession} (e.g., "Nursing")
# Years in Current Profession: {years_in_profession} (e.g., "5 years")
# Transition Goals: {transition_goals} (e.g., "Better job opportunities", "Higher salary potential")
# Areas of Tech Interest: {tech_areas_of_interest} (e.g., "Software Development", "Data Science")
# Learning Preferences: {learning_preferences} (e.g., "Online courses", "Hands-on projects")
# Learning Environment: {learning_environment} (e.g., "Self-paced learning", "Bootcamps")
# Weekly Time Commitment: {weekly_time_commitment} (e.g., "10 hours per week")
# Preferred Learning Time: {preferred_learning_time} (e.g., "Evening")
# Specific Goals: {specific_goals} (e.g., "Getting an entry-level tech job", "Building a portfolio of projects")
# Transition Timeline: {transition_timeline} (e.g., "Within 6 months")
# Anticipated Challenges: {anticipated_challenges} (e.g., "Limited time due to current job", "Financial constraints")
# Support Needed: {support_needed} (e.g., "Access to mentors or coaches", "Job placement assistance")
# Prior Tech Experience: {prior_tech_experience} (e.g., "No prior experience", "I took a coding bootcamp 2 years ago")
# Additional Information: {additional_information} (e.g., "I'm interested in learning about cybersecurity")
# Roadmap Format:
# The roadmap should be divided into clear, progressive steps that guide the user from their current level of knowledge to achieving their specific goals. Each step should include a title, a brief description, suggested resources, and an estimated timeline for completion.

# Example Roadmap Structure:
# Step 1: Introduction to Tech

# Description: Start with a foundational overview of the tech industry, including basic concepts relevant to {tech_areas_of_interest}.
# Resources: [Introduction to Tech Course], [Tech Overview Videos]
# Estimated Timeline: 2 weeks
# Step 2: Learn the Basics of {tech_areas_of_interest}

# Description: Dive into the basics of {tech_areas_of_interest}. Focus on fundamental skills and concepts.
# Resources: [Beginner Tutorials], [Introductory Textbooks]
# Estimated Timeline: 4 weeks
# Step 3: Hands-on Practice

# Description: Apply your knowledge by working on small projects or exercises. Use online platforms that offer coding challenges or practical tasks.
# Resources: [Online Coding Platforms], [Project Ideas]
# Estimated Timeline: 3 weeks
# Step 4: Intermediate Learning

# Description: Move on to more complex topics within {tech_areas_of_interest}, building on the foundation you've established.
# Resources: [Intermediate Courses], [Books and Tutorials]
# Estimated Timeline: 6 weeks
# Step 5: Build a Portfolio

# Description: Start working on real-world projects to build your portfolio. Choose projects that align with your career goals and tech interests.
# Resources: [Project Repositories], [Portfolio Building Guides]
# Estimated Timeline: 8 weeks
# Step 6: Networking and Mentorship

# Description: Begin networking with professionals in the field. Seek mentorship and join relevant tech communities.
# Resources: [Online Communities], [Mentorship Platforms]
# Estimated Timeline: Ongoing
# Step 7: Job Preparation

# Description: Prepare for job applications by refining your resume, practicing interview questions, and applying to relevant positions.
# Resources: [Resume Guides], [Interview Prep Resources]
# Estimated Timeline: 4 weeks
# Step 8: Apply for Jobs

# Description: Begin applying for entry-level positions or internships in {tech_areas_of_interest}. Use the support resources you identified earlier.
# Resources: [Job Boards], [Application Tips]
# Estimated Timeline: Ongoing
# Instructions to AI:
# Customization: Tailor each step to the user's specific background, interests, and goals. If the user has prior experience, adjust the learning path accordingly.
# Resource Selection: Suggest resources that match the user's learning preferences and environment. Include a mix of online courses, tutorials, and hands-on projects.
# Timeline: Consider the user's weekly time commitment and transition timeline when estimating the duration for each step.
# Flexibility: The roadmap should be flexible enough to accommodate the user's schedule and any anticipated challenges they mentioned.
# Encouragement: Include motivational language where appropriate to keep the user engaged and motivated throughout their learning journey.
# """