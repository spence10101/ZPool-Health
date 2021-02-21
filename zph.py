# from pySMART import Device  # Commented out until ready to implement smartctl
import subprocess


# SkipWords are the base words to filter non-disk lines
SkipWords = ["pool", "NAME", "mirror", "logs", "cache", "state", "scan",
             "config", "errors", "see", "scrub", "action", "status", "raidz"]
disks = []
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

    # Check if the line is a disk and add to the disks list
    isDisk = True
    for word in SkipWords:
        if word in line[0]:
            isDisk = False
            break
    if isDisk:
        disks.append(line)

    output.append(line)  # Save output line regardless in case we need it


# Check our disk output
for disk in disks:
    print(disk)


# Commented out smartctl test code
# disk = Device('/dev/nvme0n1')
# print(disk)
# print(disk.assessment)
