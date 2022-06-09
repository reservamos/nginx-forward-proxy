#!/usr/bin/env python3

import subprocess
import re
import datetime

docker_image = 'reservamos/nginx-forward-proxy:latest'
pattern = '/dev/xvda1(\s+[0-9.]+G){3}\s+(\d+)%\s\/'
HARD_DISK_USAGE_PERCENTAGE_LIMIT = 80

# Inspect hard disk usage.
process = subprocess.Popen(['df', '-h'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True)
stdout, stderr = process.communicate()

matches = re.search(pattern, stdout)
hard_disk_use_percentage = int(matches.group(2))

if hard_disk_use_percentage < HARD_DISK_USAGE_PERCENTAGE_LIMIT:
    exit()

# Get all docker container ids.
process = subprocess.Popen(['docker', 'ps', '-q'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
stdout, stderr = process.communicate()
docker_process_ids = stdout.split('\n')[0:-1]

for docker_process_id in docker_process_ids:
    # Stop docker process with specific id.
    process = subprocess.Popen(['docker', 'stop', docker_process_id],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)

# Initialize nginx-forward-proxy container.
process = subprocess.Popen(['docker', 'run', '--rm', '-d', '-p', '80:3128', docker_image],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
stdout, stderr = process.communicate()
print(stdout, stderr)

print('Nginx restart done on {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
