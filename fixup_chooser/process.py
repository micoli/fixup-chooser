import subprocess


def process_exec(args):
    # print(str(' '.join(args)))
    return subprocess.run(args, capture_output=True, check=True).stdout.decode("utf-8").strip("\n")
