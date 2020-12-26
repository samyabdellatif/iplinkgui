import subprocess


def dhcpclease(ifacename):
    shellcommand = r"sudo dhcpcd "+i
    process = subprocess.run(shellcommand, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    self.output = list(filter(None,map(str.strip, process.stdout.split("\n"))))
    return output