# Features
periodically gathers process metrics (for a specified amount of time)
creates a report of the gathered process metrics (in CSV format)
outputs the average for each process metric
detects possible memory leaks and raises a warning

the metrics that should be gathered for the process are:
% of CPU used
private memory used
number of open handles / file descriptors

# Usage
to start monitoring a process, run the script from the command line with the required arguments:

    process_name: The name of the process to monitor (mandatory).
    duration: The overall duration of the monitoring in seconds (mandatory).
    --interval: The sampling interval in seconds (optional, defaults to 5 seconds if not specified).

for example, open notepad.exe and put following in console:

python monitor.py "notepad.exe" 120 --interval 10

this command will monitor a process notepad.exe for 120 seconds, metrics are gathered every 10 seconds.
