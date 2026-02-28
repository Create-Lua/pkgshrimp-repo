import os
import importlib.util
import sys
import shlex

# ----------------------------
# Shell State
# ----------------------------
current_dir = os.getcwd()  # Internal shell directory
cmds_dir = os.path.join(os.getcwd(), "cmds")  # folder where command modules live
commands = {}  # cache of loaded modules

# ----------------------------
# Load a command dynamically
# ----------------------------
def load_command(cmd_name):
    cmd_path = os.path.join(cmds_dir, f"{cmd_name}.py")
    if not os.path.exists(cmd_path):
        return None

    spec = importlib.util.spec_from_file_location(cmd_name, cmd_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[cmd_name] = module
    spec.loader.exec_module(module)
    return module

# ----------------------------
# Shell prompt
# ----------------------------
def prompt(shell_state):
    # Get only the current folder name
    folder_name = os.path.basename(shell_state["current_dir"])
    if not folder_name:  # root directory
        folder_name = "/"
    return input(f"{folder_name}> ").strip()

# ----------------------------
# Main shell loop
# ----------------------------
def shell():
    shell_state = {"current_dir": os.getcwd()}

    while True:
        userinput = prompt(shell_state)
        if not userinput:
            continue

        parts = shlex.split(userinput)
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name.lower() == "exit":
            print("Exiting shell...")
            break

        if cmd_name not in commands:
            module = load_command(cmd_name)
            if module:
                commands[cmd_name] = module
            else:
                print(f"Unknown command: {cmd_name}")
                continue

        try:
            commands[cmd_name].run(args, shell_state)
        except Exception as e:
            print(f"Error running {cmd_name}: {e}")

# ----------------------------
# Run shell
# ----------------------------
if __name__ == "__main__":
    shell()