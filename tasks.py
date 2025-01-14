from crewai import Task
from tools import tool
from agents import news_researcher, news_writer

# Research task
research_task = Task(
    description=(
        "Compose a proper title (headline) for all the news related to {topic}."
        "Identify the next big trend in {topic}."
        "Focus on identifying pros and cons and the overall narrative."
        "Your final report should clearly articulate the key points,"
        "its market opportunities, and potential risks in 2-3 lines per news item."
    ),
    expected_output='A list of news items, each with a headline and 2-3 line summary.',
    tools=[tool],
    agent=news_researcher,
)

# Writing task with language model configuration
write_task = Task(
    description=(
        "Compose a proper title (headline) for all the news related to {topic}."
        "Provide a 2-3 line summary for each news item based on {topic}."
        "Focus on the latest trends and how they impact the industry."
        "The content should be concise, easy to understand, and engaging."
    ),
    expected_output='Headline: {topic}\nSummary: 2-3 lines about the news.',
    tools=[tool],
    agent=news_writer,
    async_execution=False,
    output_file='news-summaries.md'  # Output file storing news titles and summaries
)

# Example of structured output
news_data = [
    {
        "headline": "The Rise of AI in Healthcare",
        "summary": "AI is transforming healthcare by enabling faster diagnoses, personalized treatment plans, and improving patient outcomes. However, concerns about data privacy and ethical issues remain."
    },
    {
        "headline": "AI-Powered Education: The Next Frontier",
        "summary": "AI is reshaping education through adaptive learning platforms, automated grading systems, and personalized learning paths. Yet, challenges like equitable access and teacher adoption exist."
    },
]

# Save structured data to output file
def save_to_file(news_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in news_data:
            file.write(f"Headline: {item['headline']}\n")
            file.write(f"Summary: {item['summary']}\n\n")

# Save the news data
save_to_file(news_data, 'news-summaries.md')