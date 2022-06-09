import subprocess
import re

pattern = '/dev/xvda1(\s+[0-9.]+G){3}\s+(\d+)%'
process = subprocess.Popen(['df', '-h'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True)
stdout, stderr = process.communicate()

matches = re.search(pattern, stdout)
use_percentage = int(matches.group(2))

if use_percentage < 80:
    exit()

process = subprocess.Popen(['docker', 'ps', '-q'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
stdout, stderr = process.communicate()
docker_process_ids = stdout.split('\n')[0:-1]

for docker_process_id in docker_process_ids:
    process = subprocess.Popen(['docker', 'stop', docker_process_id],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout)

process = subprocess.Popen(['docker', 'run', '--rm', '-d', '-p', '80:3128', 'reservamos/nginx-forward-proxy:latest'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
stdout, stderr = process.communicate()
print(stdout, stderr)
