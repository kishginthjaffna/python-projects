# Git commit automation

import git
import os
import time

local_path = r"C:\Users\kishg\Desktop\Testing\Testing_p"
repo_url = "https://github.com/kishginthjaffna/Testing_p.git"

commit_message = f"Automated commit at {time.strftime('%Y-%m-%d %H:%M:%S')}"
branch_name = 'test2'

# Check if the directory exists and contain a valid git repo
if not os.path.exists(local_path):
    print("Cloning repo...")
    repo = git.Repo.clone_from(repo_url, local_path)
elif os.path.isdir(local_path) and not os.path.exists(os.path.join(local_path, '.git')):
    print(f"The directory {local_path} exists but is not a valid git repo. initializing repo....")
    repo = git.Repo.init(local_path)
else:
    repo = git.Repo(local_path)


# Navigate to repo
os.chdir(local_path)


# Select the branch (create if it doesn't exist)
if branch_name in repo.heads:
    repo.git.checkout(branch_name)
    print(f"Switched to existing branch '{branch_name}'")
else:
    print(f"Creating new branch '{branch_name}'...")
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()
    repo.git.push('--set-upstream', 'origin', branch_name)
    print(f"Switched to new branch '{branch_name}'")


# Check for untracked files and add them explicitly
untracked_files = repo.untracked_files

if untracked_files:
    print("Untracked files: ", untracked_files)
    for file in untracked_files:
        try:
            repo.git.add(file)
        except Exception as e:
            print(f"Error adding {file} : {e}")

# Check for untracked directories and ass a placeholder file if necessary
for root, dirs, files in os.walk(local_path):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):
            gitkeep_path = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('#Placeholder to keep empty directories in git')
                repo.git.add(gitkeep_path)
                print(f"Added .gitkeep in {dir_path}")

# Print the status to debug and see if there are any untracked or modified files
status = repo.git.status()
print("Status after adding files: ", status)


if repo.is_dirty():
    try:
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push(branch_name)  
        print(f"Changes successfully committed and pushed to '{branch_name}'.")
    except Exception as e:
        print(f"Error during committing and pushing the changes: {e}")
else:
    print("No changes in the repo to commit")

