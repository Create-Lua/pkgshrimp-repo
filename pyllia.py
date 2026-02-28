def run(args, shell_state):
    if not args:
        print("Usage: pyllia [--version|--credits]")
        return

    flag = args[0]

    if flag == "--version":
        print("Pyllia version 0.1.0")

    elif flag == "--credits":
        print("Pyllia created by Alex")

    else:
        print("Invalid usage.")
