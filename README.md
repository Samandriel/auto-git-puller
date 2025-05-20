# Auto Git Pull

A Python script that automatically pulls changes from a remote Git repository whenever new commits are pushed to the specified branch.

## Features

- Monitors a Git repository for new commits on a specified branch
- Automatically pulls changes when detected
- Configurable check interval
- Detailed logging

## Requirements

- Python 3.6+
- Git installed and configured

## Usage

```bash
python auto_git_pull.py /path/to/your/repo [--branch BRANCH] [--interval SECONDS]
```

### Arguments

- `repo_path`: Path to the Git repository (required)
- `--branch`, `-b`: Branch to monitor (default: main)
- `--interval`, `-i`: Check interval in seconds (default: 60)

### Example

```bash
# Check for changes every 5 minutes on the main branch
python auto_git_pull.py /path/to/your/repo --interval 300

# Monitor the develop branch instead
python auto_git_pull.py /path/to/your/repo --branch develop
```

## Running in the Background

### On macOS/Linux

To run the script in the background:

```bash
nohup python auto_git_pull.py /path/to/your/repo &
```

To stop the script:
```bash
ps aux | grep auto_git_pull.py
kill <PID>
```

### Setting up as a Service

For a more permanent solution, you can set up the script as a service using systemd (Linux) or launchd (macOS).

## Logs

The script creates a log file named `git_puller.log` in the directory where the script is run.
