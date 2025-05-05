# Flug - Flugsicherung
A Python based CLI tool for scheduling and orchestration of processes

## Quick start

1) Install flug globally
```
pipx install flug
```

2) Define a yaml file in your project, such as my_task.atc.yaml
```
namespace: production.example.task
command:
    - echo "running with flug"
    - python my_task.py
schedule:
    time_of_day
        - 1:00:00
```

3) Add your task with Flug
```
flug add my_task.atc.yaml
```

4) Running `flug list` will show your task has indeed been added. You can run this command to view all registered flug tasks and some information about their status. We can see the working directory of the task defaulted to the location of our my_task.atc.yaml file. We also see that while the task has been added, it is not active. A task will not run unless it is active.
```
$> flug list

ID  Namespace                Active  Dir                     
1   production.example.task  False   /home/user/code/test_project
```

5) Start your task.
```
flug start my_task.atc.yaml
```

Now if we run `flug list` again, we see the task is active
```
$> flug list

ID  Namespace                Active  Dir                     
1   production.example.task  True    /home/user/code/test_project
```
