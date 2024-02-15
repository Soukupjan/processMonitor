import argparse
import csv
import time
import psutil

#take process_name as argument, loop through the processes found by psutil.process_iter and pick first one with name == process_name, return it else return none
def find_process_by_name(process_name):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == process_name:
            return proc
    return None

#take proccess found previously as argument, use psutil functions, cpu_percent gives usage over interval, memory_info().rss gives resident set size (memory usage) 
#then we take handles, in windows its num_handles, elsewhere num_fds is used
def gather_metrics(process):
    cpu_percent = process.cpu_percent(interval=1)
    memory_info = process.memory_info().rss
    try:
        if hasattr(process, 'num_handles'):
            handles = process.num_handles()
        else:
            handles = process.num_fds()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        handles = 'N/A'
    return cpu_percent, memory_info, handles

#create csv file, write header and then loop through metrics and write them down
def generate_report(metrics, filename):
    headers = ['Timestamp', 'CPU %', 'Memory (bytes)', 'Handles/FDs']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i, (cpu, memory, handles) in enumerate(metrics):
            writer.writerow([time.time(), cpu, memory, handles])

#calculate averages, sum all values and divide by number of values
def calculate_averages(metrics):
    avg_cpu = sum([m[0] for m in metrics]) / len(metrics)
    avg_memory = sum([m[1] for m in metrics]) / len(metrics)
    print(f"Average CPU Usage: {avg_cpu}%")
    print(f"Average Memory Usage: {avg_memory} bytes")

#checks whether memory usage keeps rising over time, found online
def detect_memory_leak(metrics):
    memory_usage = [m[1] for m in metrics]
    if len(memory_usage) > 1 and all(memory_usage[i] <= memory_usage[i + 1] for i in range(len(memory_usage) - 1)):
        print("Possible memory leak, memory usage consistently increasing")


def monitor_process(process_name, duration, interval):
    process = find_process_by_name(process_name)
    if process is None:
        print(f"process'{process_name}' not found.")
        return
    
    start_time = time.time()
    metrics = []
    
    while (time.time() - start_time) < duration:
        metrics.append(gather_metrics(process))
        time.sleep(interval)
    
    generate_report(metrics, f"{process_name}_report.csv")
    calculate_averages(metrics)
    detect_memory_leak(metrics)

def main():
    parser = argparse.ArgumentParser(description='monitoring app for process resources')
    parser.add_argument('process_name', type=str, help='name of the process you want to monitor')
    parser.add_argument('duration', type=int, help='for how long')
    parser.add_argument('--interval', type=int, default=5, help='interval in seconds (default = 5)')
    
    args = parser.parse_args()
    
    monitor_process(args.process_name, args.duration, args.interval)

if __name__ == "__main__":
    main()
