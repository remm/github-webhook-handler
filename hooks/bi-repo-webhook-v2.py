import github

token = '049140259575365d2299e467c4fd1be81d3696c2'
g = github.Github(token)

repo = g.get_user().get_repo("github-webhook-handler-test")
print(repo)
file = repo.get_file_contents("/wix-bi-dev/pom.xml")
raw_data = file.decoded_content
print(raw_data)

# update
# repo.update_file("/your_file.txt", "your_commit_message", "your_new_file_content", file.sha)
