from collections import defaultdict
def analyze_language(repos):
    count = defaultdict(int)
    output = []
    for repo in repos:
        language = repo.get('language') # Use get as a safe fail incase language was not given, the app continues running
        if language:
            count[language] += 1
    total_used = sum(count.values())
    for key in count.keys():
        percentage_used = (count[key]/total_used) * 100
        output.append((key,round(percentage_used,2)))
    return sorted(output, key=lambda x: x[1], reverse=True)
    