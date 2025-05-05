# Flug - Flugsicherung
A Python based CLI tool for scheduling and orchestration of processes

## Quick start

### 1. Install flug
It is generally recommended to install flug globally. You can install globally via pipx.
```
pipx install flug
```

### 2. Define your task
Create a yaml file in your project, such as my_task.atc.yaml. At a minimum, a flug task must specify a unique namespace, a command, and a schedule. There are many ways to define a schedule, but for this example, lets say we want to run the task every day at 1:00am.
```
namespace: production.example.task
command:
    - echo "running with flug"
    - python my_task.py
schedule:
    time_of_day
        - 1:00:00
```

### 3. Register the task
Flug needs to know your task exists. To do this, you can add your task to flug using the below command.
```
flug add my_task.atc.yaml
```

### 4. Verify your task
Running `flug list` will show your task has indeed been added. You can run this command to view all registered flug tasks and some information about their status. We can see the working directory of the task defaulted to the location of our my_task.atc.yaml file. We also see that while the task has been added, it is disabled. A task will not run unless it is enabled.
```
$> flug list

ID  Namespace                Enabled  Dir                     
1   production.example.task  False    /home/user/code/test_project
```

### 5. Enable your task.
A flug task has two states, enabled and disabled. In order for the scheduled executions to actually run, the task must be enabled.
```
flug enable my_task.atc.yaml
```

Tip: When adding task you can also activate it in the same command by adding a -e flag
```
flug add -e my_task.atc.yaml
```

Now if we run `flug list` again, we see the task is enabled
```
$> flug list

ID  Namespace                Enabled  Dir                     
1   production.example.task  True     /home/user/code/test_project
```
