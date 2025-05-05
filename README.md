# atc
Air Traffic Control - Python based CLI tool for scheduling and orchestration of processes  


## Quick start

1) Install flug globally
`pipx install flug`

2) Define a .atc.yaml file
```
namespace: production.example.task
command:
    - echo "running with flug"
    - python my_task.py
schedule:
    time_of_day
        - 1:00:00
```
