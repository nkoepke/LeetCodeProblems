import requests
import json
from bs4 import BeautifulSoup  # To clean HTML content

# LeetCode GraphQL API endpoint
url = "https://leetcode.com/graphql"

# GraphQL query to fetch problem details
query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    content
    difficulty
    likes
    dislikes
    topicTags {
      name
      slug
    }
  }
}
"""

# List of problem slugs (replace with your own list)

# Path to your JSON file
file_path = "leetcode_problem_slugs.json"

# Read the JSON file and store it as a variable
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

problem_slugs = data
'''
[
    "two-sum",
    "add-two-numbers",
    "longest-substring-without-repeating-characters",
    "median-of-two-sorted-arrays",
    "longest-palindromic-substring",
    "zigzag-conversion",
    "binary-tree-upside-down"
]
'''

# HTTP headers
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Function to fetch problem details
def fetch_problem_details(slug):
    response = requests.post(url, json={"query": query, "variables": {"titleSlug": slug}}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("question", {})
    else:
        print(f"Failed to fetch problem: {slug} (Status Code: {response.status_code})")
        return None

# Function to clean HTML content
def clean_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text()
    return ""

# Fetch details for each problem in the list
problems = []
q = 1
for slug in problem_slugs:
    problem_details = fetch_problem_details(slug)
    if problem_details:
        # Append accessible problem data
        print(f"slug ({q}/{len(problem_slugs)}) {slug}")
        problems.append({
            "id": problem_details.get("questionId"),
            "title": problem_details.get("title"),
            "difficulty": problem_details.get("difficulty"),
            "likes": problem_details.get("likes"),
            "dislikes": problem_details.get("dislikes"),
            "tags": [tag["name"] for tag in problem_details.get("topicTags", [])],
            "description": clean_html(problem_details.get("content")),
            "accessible": True,
            "slug": slug
        })
    else:
        # Append inaccessible problem data
        problems.append({
            "slug": slug,
            "description": "",
            "accessible": False
        })
    q = q + 1

# Save the collected data to a JSON file
output_file = "leetcode_problems_cleaned.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(problems, f, indent=4)

print(f"Problem details saved to {output_file}")
