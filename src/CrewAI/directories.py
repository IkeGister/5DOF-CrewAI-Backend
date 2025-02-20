"""
Directories for Various Templates
==================================

This file contains different directories that can be used for various purposes,
such as customer engagement, customer care, software engineering assistance, and ticket search assistance.
"""

# Directory for Customer Engagement Guide
customer_engagement_guide = {
    "title": "Customer Engagement Guide for Small Businesses",
    "introduction": (
        "For small businesses, personal touch and understanding local needs are paramount. "
        "Your message should reflect an understanding of their market, the challenges they face, "
        "and how your solutions make their daily operations smoother and more efficient."
    ),
    "key_points": [
        "Personalization: Show that you understand their specific business needs.",
        "Efficiency: Highlight how your solutions can streamline operations.",
        "Community: Emphasize your commitment to supporting local businesses."
    ],
    "template_message": (
        "Hello [Name],\n\n"
        "As a local business owner, your dedication to [specific aspect of their business, "
        "e.g., providing excellent customer service, offering high-quality products] truly stands out. "
        "At [Your Company], we offer solutions that can help businesses like [Business Name] become even "
        "more efficient and effective.\n\n"
        "[Describe a specific feature of your product/service and how it solves a problem they face].\n\n"
        "We would love to discuss how we can be part of your success story.\n\n"
        "Warm regards,\n[Your Name]"
    )
}

# Directory for Customer Care Operator Guidelines
customer_care_guidelines = {
    "title": "Customer Care Operator Guidelines",
    "introduction": (
        "Effective communication is key to customer satisfaction. This guide provides "
        "essential tips for addressing customer inquiries and concerns."
    ),
    "key_points": [
        "Empathy: Always show understanding and compassion.",
        "Clarity: Provide clear and concise information.",
        "Follow-up: Ensure to follow up on unresolved issues."
    ],
    "template_message": (
        "Hello [Customer Name],\n\n"
        "Thank you for reaching out to us. We appreciate your feedback and are here to assist you. "
        "Please let us know how we can help you further.\n\n"
        "Best regards,\n[Your Name]"
    )
}

# Directory for Software Engineer Assistance
software_engineer_assistance = {
    "title": "Software Engineer Assistance Guide",
    "introduction": (
        "As a software engineer, understanding the capabilities of your tools can greatly enhance productivity. "
        "This guide outlines how you can assist users with their GitHub repositories."
    ),
    "key_points": [
        "Code Review: Offer insights on code quality and best practices.",
        "Issue Tracking: Help users manage and resolve issues effectively.",
        "Collaboration: Encourage collaboration through pull requests and discussions."
    ],
    "template_message": (
        "Hello [User],\n\n"
        "I noticed you have some interesting projects on your GitHub repository. "
        "I can assist you with code reviews, issue tracking, and enhancing collaboration. "
        "Let me know how I can help!\n\n"
        "Best,\n[Your Name]"
    )
}

# Directory for Travel Assistant Communication
travel_assistant_guide = {
    "title": "Travel Assistant Communication Guide",
    "introduction": (
        "This guide provides instructions for the AI assistant on how to collect the necessary information "
        "from users to trigger the TicketSearchTool and how to convey the information received after collection."
    ),
    "key_points": [
        "Clarity: Ensure that each question is clear and concise.",
        "Sequential Questions: Ask questions one at a time to avoid overwhelming the user.",
        "Confirmation: After collecting each piece of information, confirm with the user before proceeding.",
        "Error Handling: If the user provides invalid data, politely ask them to re-enter the information.",
        "Professional Tone: Maintain a friendly and professional tone throughout the interaction.",
        "Information Presentation: After gathering information, summarize it clearly for the user, highlighting key points such as flight options, weather conditions, and accommodations."
    ],
    "template": {
        "Full Name": {
            "question": "Could you please provide your full name?",
            "confirmation": "Just to confirm, your full name is [User's Response]. Is that correct?"
        },
        "Email Address": {
            "question": "What email address would you like to use for sending the tickets?",
            "confirmation": "You provided the email address [User's Response]. Is that correct?"
        },
        "Traveling From": {
            "question": "What is your departure location?",
            "confirmation": "You are traveling from [User's Response]. Is that correct?"
        },
        "Traveling To": {
            "question": "What is your destination location?",
            "confirmation": "You are traveling to [User's Response]. Is that correct?"
        },
        "Travel Date": {
            "question": "What is your travel date? Please provide it in YYYY-MM-DD format.",
            "confirmation": "Your travel date is [User's Response]. Is that correct?"
        },
        "Return Date": {
            "question": "Do you have a return date? If so, please provide it in YYYY-MM-DD format.",
            "confirmation": "Your return date is [User's Response]. Is that correct?"
        },
        "Flight Class": {
            "question": "What class of travel would you prefer? (e.g., economy, business)",
            "confirmation": "You prefer [User's Response] class. Is that correct?"
        },
        "Luggage Number": {
            "question": "How many pieces of luggage will you be taking?",
            "confirmation": "You mentioned [User's Response] pieces of luggage. Is that correct?"
        },
        "Travel Companions": {
            "question": "How many travel companions will be joining you?",
            "confirmation": "You will be traveling with [User's Response] companions. Is that correct?"
        },
        "Companion Type": {
            "question": "Are any of your companions minors or pets? If it's a pet, what kind?",
            "confirmation": "You mentioned [User's Response] as the type of companion. Is that correct?"
        },
        "Preferred Flight": {
            "question": "Do you have a preferred flight, or would you like an open search?",
            "confirmation": "You prefer [User's Response] for the flight. Is that correct?"
        }
    },
    "final_confirmation": (
        "Thank you for providing the information. Here’s what I have collected:\n"
        "- Full Name: [User's Full Name]\n"
        "- Email: [User's Email]\n"
        "- Traveling From: [User's Traveling From]\n"
        "- Traveling To: [User's Traveling To]\n"
        "- Travel Date: [User's Travel Date]\n"
        "- Return Date: [User's Return Date]\n"
        "- Flight Class: [User's Flight Class]\n"
        "- Luggage Number: [User's Luggage Number]\n"
        "- Travel Companions: [User's Travel Companions]\n"
        "- Companion Type: [User's Companion Type]\n"
        "- Preferred Flight: [User's Preferred Flight]\n\n"
        "Is everything correct? If so, I will proceed to search for tickets."
    ),
    "searching_message": (
        "Thank you for your patience while I search for the best ticket options for you. "
        "This may take a moment, but I will keep you updated with the results as soon as I have them."
    ),
    "information_summary": (
        "Here is a summary of the information collected:\n"
        "- Available Flight Options: [Flight Options]\n"
        "- Weather Conditions: [Weather Conditions]\n"
        "- Hotel Options: [Hotel Options]\n"
        "- Tourist Attractions: [Tourist Attractions]\n\n"
        "Please review this information and let me know if you have any questions or need further assistance."
    )
} 