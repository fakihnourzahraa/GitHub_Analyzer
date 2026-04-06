import requests #https calls
from rich.console import Console
from rich.table import Table #colors
from groq import Groq
from dotenv import load_dotenv #for env
import os #for env
from rich.live import Live
from rich.spinner import Spinner

load_dotenv() 
console = Console()
#console for HTTP calls and table for terminal
client = Groq(api_key=os.getenv("API_KEY"))
def get_user(username):
	url = f"https://api.github.com/users/{username}"
	response = requests.get(url)
	if (response.status_code != 200):
		console.print("[red]User not found![/red]")
		return None
	return response.json()

def get_repos(username):
	url = f"https://api.github.com/users/{username}/repos?per_page=100"
	response = requests.get(url)
	if (response.status_code != 200):
		console.print("[red]Could not fetch repo!![/red]")
		return [] #so it doesnt crash when trying to loop
	return response.json()

def show_profile(user):
	console.print(f"[bold cyan]👤 {user['name'] or user['login']}[/bold cyan]")
	console.print(f"[dim]{user['bio'] or 'No bio'}[/dim]")
	console.print(f"📦 Public Repos: [yellow]{user['public_repos']}[/yellow]")
	console.print(f"👥 Followers: [yellow]{user['followers']}[/yellow]\n")

def show_repos(repos):
	table = Table(title="Top 10 Repositories")
	table.add_column("Name", style="cyan")
	table.add_column("Language", style="magenta")
	sorted_repos = sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)[:10]
	for repo in sorted_repos:
		table.add_row( repo['name'], repo['language'] or 'N/A',)
	console.print(table)

def get_top_language(repos):
    languages = {}
    for repo in repos:
        lang = repo['language']
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    if not languages:
        return "N/A"
    return max(languages, key=languages.get)


def analyze_profile(user, repos, job_requirements):
	top_lang = get_top_language(repos)
	languages = list(set(r['language'] for r in repos if r['language']))

	prompt = f"""
    GitHub Profile:
    - Name: {user['name'] or user['login']}
    - Public Repos: {user['public_repos']}
    - Followers: {user['followers']}
    - Top Language: {top_lang}
    - Languages used: {', '.join(languages)}

    Job Requirements:
    {job_requirements}
    
 Instructions:
    - If the job requirements are vague, nonsensical, or clearly not a real role, politely say so and stop.
    - Speak directly to the person (second person, "you/your").
    - Be honest, short, and human — not robotic or overly formal.
    - Only mention followers if the role has a social/community aspect.
    - You can use emojis but don't overdo it.
	- Be direct and concise
    Analyze in this order:
    1. How strong is this profile for the role?
    2. What's missing or needs work?
    3. Two (or more if needed) concrete action points they can act on today.

    End with a good luck message and "Thank you for using GitHub_Summary! 🚀"
    """

	response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
	return response.choices[0].message.content

def main():
	username = input("Enter GitHub username: ")
	job_requirements = input("Enter job requirements: ")

	user = get_user(username)
	if not user:
		return

	repos = get_repos(username)

	show_profile(user)
	show_repos(repos)

	top_lang = get_top_language(repos)
	console.print(f"🏆 Top Language: [bold green]{top_lang}[/bold green]\n")
	with Live(Spinner("dots", text="Analyzing your profile"), refresh_per_second=7):
		analysis = analyze_profile(user, repos, job_requirements)
	console.print("done!\n")
	console.print(analysis)
    # console.print("[bold yellow]🤖 AI Analysis...[/bold yellow]\n")
    # analysis = analyze_profile(user, repos, job_requirements)
    # console.print(analysis)
    
main()