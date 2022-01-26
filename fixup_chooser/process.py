import subprocess


def process_exec(args):
    #print(str(' '.join(args)))
    try:
        return subprocess.run(args, capture_output=True, check=True).stdout.decode("utf-8").strip("\n")
    except subprocess.CalledProcessError as error:
        error.cmd = '%s\n%s' % (error.cmd, str(' '.join(args)))
        raise error
