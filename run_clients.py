import subprocess

from pathlib import Path

import pyautogui
import pywinauto
import time

from ahk import AHK

ahk = AHK()
## CHANGE THESE TWO VARIABLES TO YOUR OWN JAVA AND SQUIRE.JAR LOCATION!!!!!!!!!!!!
JAVA_PATH = "java"

SQUIRE_JAR_PATH = "squire.jar"
## CHANGE THESE TWO VARIABLES TO YOUR OWN JAVA AND SQUIRE.JAR LOCATION!!!!!!!!!!!!
procs: list[subprocess.Popen] = []
def run_clients():
    with Path("accounts.txt").open() as f:

        clients = f.read().splitlines()
        clients = [c.strip() for c in clients]
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--world", type=int, default=0, help="World to log all accounts into")
        parser.add_argument("--proxy", type=str, default=None, help="Proxy to use for all accounts")
        parser.add_argument("--skip", type=bool, default=False, help="automatically skip auth and nightly")
        args = parser.parse_args()
        main_arg = f"{JAVA_PATH} -XX:+DisableAttachMechanism -Dsun.java2d.noddraw=true -Xmx4G -Xss2m -XX:CompileThreshold=1500 -jar -Drunelite.launcher.nojvm=true {SQUIRE_JAR_PATH}"
        if args.skip:
            main_arg = f"{main_arg} --skip-auth --nightly"
        for client in clients:
            if client.startswith("#"):
                continue
            launch_arg = main_arg
            accinfo = client.split(",")
            print(accinfo)
            username = accinfo[0].strip()
            password = accinfo[1].strip()
            if len(accinfo) > 2:
                world = accinfo[2].strip()
            if len(accinfo) > 3:
                proxy = accinfo[3].strip()
            if args.world != 0:
                print(f"adding parameter world arg {args.world}")
                launch_arg = f"{launch_arg} --world={args.world}"
            elif world:
                print(f"adding account world arg {world}")
                launch_arg = f"{launch_arg} --world={world}"
            if args.proxy is not None:
                print(f"adding parameter world arg {args.proxy}")
                launch_arg = f"{launch_arg} --proxy={args.proxy}"
            elif proxy:
                print(f"adding account world arg {proxy}")
                launch_arg = f"{launch_arg} --proxy={proxy}"
            userproperties =Path().home().joinpath(f".squire/{username}.squire.properties")
            print(userproperties.absolute())
            squireprops = Path().home().joinpath(".squire/squire.properties")
            print(squireprops.absolute())
            if not userproperties.exists():
                import shutil
                shutil.copy(squireprops.absolute(), userproperties.absolute())
            run_arg = f"{launch_arg} --account={username}:{password}"# --profile={userproperties.absolute()}"
            print(run_arg)
            print(run_arg.split(" "))

            proc: subprocess.Popen = subprocess.Popen(run_arg.split(" "), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            procs.append(proc)
        # time.sleep(1)
# def window_filter(window):
#     return "java" in window.get('process')
#
# attempts = 0
# # run_clients()
# # time.sleep(30)
# # while attempts < 10:
# for window in ahk.windows():
#     # print(window.class_name, window.title, window.text, window.process)
#     if "java" in window.process:
#         if not window.is_active():
#             print(f"window {window.title} is not active, activating")
#             window.activate()
#         ahk.send_input("{Enter}")
#         ahk.send_input("{Enter}")
#     # time.sleep(2)
run_clients()