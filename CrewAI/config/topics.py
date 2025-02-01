CONTENT_TOPICS = {
    "technology": [
        "Artificial Intelligence",
        "Machine Learning",
        "Blockchain",
        "Internet of Things",
        "Cybersecurity"
    ],
    "business": [
        "Digital Transformation",
        "Entrepreneurship",
        "Project Management",
        "Marketing Strategy",
        "Financial Technology"
    ],
    "science": [
        "Climate Change",
        "Quantum Computing",
        "Biotechnology",
        "Space Exploration",
        "Renewable Energy"
    ]
}

def get_topic(category: str, index: int = 0) -> str:
    """
    Get a specific topic from a category
    """
    return CONTENT_TOPICS.get(category, [])[index]

def get_all_topics(category: str = None) -> list:
    """
    Get all topics or topics from a specific category
    """
    if category:
        return CONTENT_TOPICS.get(category, [])
    return [topic for topics in CONTENT_TOPICS.values() for topic in topics] 