import asyncio
import multiprocessing
import os
import subprocess
import sys
import xml.dom.minidom
import argparse
from subprocess import DEVNULL, PIPE


style_error_message = []


def download_checkstyle():
    # TODO: Download checkstyle jar
    pass


def check_java():
    """
    Check whether Java is working
    """
    try:
        subprocess.check_output(["java", "-version"], stderr=DEVNULL)
    except Exception as e:
        print("FATAL: Java not working")
        print(e)
        return False
    return True


def check_checkstyle(checkstyle_jar, checkstyle_config):
    """
    Check checkstyle jar file and config
    """
    if not os.path.isfile(checkstyle_jar):
        print("cannot find checkstyle jar")
        return False
    if not os.path.isfile(checkstyle_config):
        print("cannot find checkstyle config")
        return False
    return True


def handleCheckstyle(checkstyle):
    """
    Arguments: Node <checkstyle>
    """
    files = checkstyle.getElementsByTagName("file")
    handleFile(files[0])


def handleFile(file):
    """
    Arguments: Node <file>
    """
    global style_error_message
    errors = file.getElementsByTagName("error")
    file_name = file.getAttribute("name")
    error_messages = handleError(errors)
    style_error_message.append((file_name, error_messages))


def handleError(errors):
    """
    Arguments: Node <errors>
    """
    error_messages = []
    for err in errors:
        error_messages.append("Line {}: {}".format(
            err.getAttribute("line"), err.getAttribute("message")))
    return error_messages


def print_summary():
    total_error_count = 0
    print("--------CheckStyle Summary--------")
    for filename, msg in style_error_message:
        if len(msg) > 0:
            total_error_count = total_error_count+len(msg)
            print('Found %d Error in %s' % (len(msg), filename))
            for i in msg:
                print(i)
    print("Total style errors: %d" % total_error_count)


async def execute_check(checkstyle_jar, checkstyle_config, src_path):
    print('Checking', src_path)
    args = ["-jar", checkstyle_jar,
            "-f", "xml",
            "-c", checkstyle_config, src_path]
    proc = await asyncio.create_subprocess_exec('java',
                                                *args,
                                                stdout=PIPE,
                                                stderr=DEVNULL)
    (stdout_data, _) = await proc.communicate()
    # print(stdout_data.decode())
    dom = xml.dom.minidom.parseString(stdout_data.decode())
    handleCheckstyle(dom)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--jar', default="bin/checkstyle-8.12-all.jar", help="Checkstyle JAR file")
    parser.add_argument('--config', default="bin/config.xml",
                        help="specifies the location of the file that defines the configuration modules.")
    parser.add_argument(
        "directory", help="directory that contains the projects")
    opt = parser.parse_args()
    checkstyle_jar = opt.jar
    checkstyle_config = opt.config
    print(opt)
    if not check_java():
        exit()
    if not check_checkstyle(checkstyle_jar, checkstyle_config):
        print(parser.format_help())
        exit()
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    homework_dirs = filter(os.path.isdir, os.scandir(opt.directory))
    tasks_async = []
    for i in homework_dirs:
        src_path = os.path.join(i.path, "src")
        if os.path.isdir(src_path):
            tasks_async.append(execute_check(
                checkstyle_jar, checkstyle_config, src_path))
        else:
            print("Skipping", i.path)
    loop.run_until_complete(asyncio.wait(tasks_async))
    loop.close()
    print_summary()
