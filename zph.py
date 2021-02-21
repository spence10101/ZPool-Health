# from pySMART import Device  # Commented out until ready to implement smartctl
import subprocess
import re

# SkipWords are the base words to filter non-disk lines
SkipWords = ["pool", "NAME", "mirror", "logs", "cache", "state", "scan",
             "config", "errors", "see", "scrub", "action", "status", "raidz"]
disks = {}
bypartition = []
byuuid = []
output = []

# Run zpool status command and split the output into lines
rawout = subprocess.check_output(["zpool", "status"]).decode().split('\n')

# Processing the zpool output
for line in rawout:
    # Preprocessing the lines
    if line.strip() == '':  # Skip blank lines
        continue
    line = line.split()
    if line[0] == "pool:":  # Add pools to lines to skip
        SkipWords.append(line[1])

    # Check if the line is a disk/partition and add to the proper list or dictionary
    isDisk = True
    for word in SkipWords:
        if word in line[0]:
            isDisk = False
            break
    if isDisk:
        if '-' in line[0]:
            byuuid.append(line)
        elif line[0].isalpha():
            disks[line[0]] = line[1:]
        else:
            bypartition.append(line)

    output.append(line)  # Save output line regardless in case we need it

# Run blkid command and split the output into lines
rawout = subprocess.check_output(["blkid"]).decode().split('\n')

# Turn UUIDs into partition references
for line in rawout:
    for part in byuuid:
        if part[0] in line:
            part[0] = line.split(": ")[0].split('/')[2]
            bypartition.append(part)

# Turn partitions into disks
for part in bypartition:
    part[0] = re.sub('\d', '', part[0])
    disks[part[0]] = part[1:]

# Check our disk output
for disk in sorted(disks.items()):
    print(disk)

# Commented out smartctl test code
# disk = Device('/dev/nvme0n1')
# print(disk)
# print(disk.assessment)
