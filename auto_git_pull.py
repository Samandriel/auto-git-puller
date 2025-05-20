#!/usr/bin/env python3
import os
import time
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("git_puller.log"),
        logging.StreamHandler()
    ]
)

class GitPuller:
    def __init__(self, repo_path, branch="main", check_interval=60):
        """
        Initialize the GitPuller.
        
        Args:
            repo_path: Path to the git repository
            branch: Branch to monitor (default: main)
            check_interval: How often to check for changes in seconds (default: 60)
        """
        self.repo_path = os.path.abspath(repo_path)
        self.branch = branch
        self.check_interval = check_interval
        self.last_commit_hash = None
        
        # Validate that the path is a git repository
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            raise ValueError(f"The path {self.repo_path} is not a git repository")
        
        logging.info(f"Monitoring repository at {self.repo_path} on branch {self.branch}")
        
    def get_latest_commit_hash(self):
        """Get the latest commit hash from the remote repository."""
        try:
            # Fetch the latest changes without merging
            subprocess.run(
                ["git", "fetch", "origin", self.branch], 
                cwd=self.repo_path, 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Get the latest commit hash from the remote
            result = subprocess.run(
                ["git", "rev-parse", f"origin/{self.branch}"],
                cwd=self.repo_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"Error getting latest commit hash: {e}")
            logging.error(f"Command output: {e.stderr}")
            return None
    
    def pull_changes(self):
        """Pull the latest changes from the remote repository."""
        try:
            logging.info("Pulling latest changes...")
            result = subprocess.run(
                ["git", "pull", "origin", self.branch],
                cwd=self.repo_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logging.info(f"Pull successful: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error pulling changes: {e}")
            logging.error(f"Command output: {e.stderr}")
            return False
    
    def start_monitoring(self):
        """Start monitoring the repository for changes."""
        logging.info(f"Starting to monitor repository for changes every {self.check_interval} seconds")
        
        # Get the initial commit hash
        self.last_commit_hash = self.get_latest_commit_hash()
        if self.last_commit_hash:
            logging.info(f"Initial commit hash: {self.last_commit_hash}")
        
        try:
            while True:
                current_hash = self.get_latest_commit_hash()
                
                if current_hash and current_hash != self.last_commit_hash:
                    logging.info(f"New commit detected: {current_hash}")
                    logging.info(f"Previous commit: {self.last_commit_hash}")
                    
                    if self.pull_changes():
                        self.last_commit_hash = current_hash
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor a git repository and pull changes automatically")
    parser.add_argument("repo_path", help="Path to the git repository")
    parser.add_argument("--branch", "-b", default="main", help="Branch to monitor (default: main)")
    parser.add_argument("--interval", "-i", type=int, default=60, help="Check interval in seconds (default: 60)")
    
    args = parser.parse_args()
    
    puller = GitPuller(args.repo_path, args.branch, args.interval)
    puller.start_monitoring()
