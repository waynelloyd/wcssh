#!/usr/bin/env python3
"""
wcssh.py — Warp-native multi-SSH launcher that opens a new window, splits panes, and optionally enables synchronized input.
"""

import argparse
import shlex
import subprocess
import sys
import time
from typing import List, Optional

__version__ = "1.0.0"


def run_applescript(script: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["osascript", "-e", script], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def activate_warp():
    run_applescript('tell application "Warp" to activate')


def warp_new_window():
    # Open a new Warp window (CMD-N)
    activate_warp()
    time.sleep(0.05)
    run_applescript('tell application "System Events" to keystroke "n" using {command down}')


def warp_split_right():
    # Split the current pane to the right (CMD-D)
    run_applescript('tell application "System Events" to keystroke "d" using {command down}')


def warp_type_and_enter(cmd: str):
    safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
    applescript = f'tell application "System Events" to keystroke "{safe_cmd}"'
    run_applescript(applescript)
    time.sleep(0.02)
    run_applescript('tell application "System Events" to key code 36')  # Enter


def warp_enable_broadcast():
    # Enable Warp synchronized input using keyboard shortcut only
    activate_warp()
    time.sleep(0.3)
    
    # Use keyboard shortcut: Option + Command + I
    run_applescript('tell application "System Events" to keystroke "i" using {option down, command down}')
    time.sleep(0.1)


def read_hosts_from_stdin() -> List[str]:
    if sys.stdin.isatty():
        return []
    data = sys.stdin.read()
    raw = [p.strip() for p in data.replace("\n", ",").replace("\t", ",").split(",")]
    return [h for h in raw if h]


def parse_and_flatten_hosts(hosts_list: List[str]) -> List[str]:
    """Takes a list of strings and splits them by space or comma, returning a flat list of hosts."""
    if not hosts_list:
        return []
    
    all_hosts_str = " ".join(hosts_list)
    all_hosts_str = all_hosts_str.replace(",", " ")
    
    return [host.strip() for host in all_hosts_str.split() if host.strip()]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="wcssh — Warp multi-SSH launcher (macOS)")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("hosts", nargs="*", help="Target hosts")
    p.add_argument("--user", "-u", help="SSH username")
    p.add_argument("--port", "-p", default="22", help="SSH port (default 22)")
    p.add_argument("--identity", "-i", help="Path to SSH private key")
    p.add_argument("--ssh-opts", default="", help="Additional raw ssh options string")
    p.add_argument("--delay", type=float, default=0.2, help="Delay between creating pane/tab and sending command")
    p.add_argument(
        "--no-broadcast",
        action="store_true",
        help="Disable Warp synchronized input (broadcast) - enabled by default",
    )
    return p.parse_args(argv)


def build_ssh_command(host: str, user: Optional[str], port: str, identity: Optional[str], ssh_opts: str) -> str:
    target = f"{user}@{host}" if user else host
    parts = ["ssh"]
    if port:
        parts += ["-p", str(port)]
    if identity:
        parts += ["-i", identity]
    if ssh_opts:
        parts += shlex.split(ssh_opts)
    parts += [target]
    return " ".join(shlex.quote(p) for p in parts)


def main(argv: Optional[List[str]] = None):
    if sys.platform != "darwin":
        print("This script only runs on macOS.", file=sys.stderr)
        sys.exit(2)

    args = parse_args(argv)
    stdin_hosts = read_hosts_from_stdin()
    cli_hosts = parse_and_flatten_hosts(args.hosts or [])
    hosts = stdin_hosts + cli_hosts
    if not hosts:
        # If no hosts are provided, and version is requested, let argparse handle it.
        if not (len(sys.argv) > 1 and sys.argv[1] == '--version'):
             print("No hosts provided.", file=sys.stderr)
             sys.exit(1)
        else:
            # argparse with action='version' will exit here, so we don't need to.
            pass


    ssh_cmds = [build_ssh_command(h, args.user, args.port, args.identity, args.ssh_opts) for h in hosts]

    # Open a new Warp window
    warp_new_window()
    time.sleep(args.delay + 0.3)  # extra delay for window to appear
    activate_warp()
    time.sleep(0.05)

    # Type first SSH command in the first pane
    if ssh_cmds:
        warp_type_and_enter(ssh_cmds[0])
        time.sleep(args.delay)

    # Split panes for remaining hosts
    for cmd in ssh_cmds[1:]:
        warp_split_right()
        time.sleep(args.delay + 0.25)  # ensure split pane is ready
        activate_warp()
        time.sleep(0.05)
        warp_type_and_enter(cmd)
        time.sleep(args.delay)

    # Enable broadcast by default unless disabled
    if not args.no_broadcast and len(ssh_cmds) > 1:
        time.sleep(1.0)  # Give more time for all panes to be ready
        warp_enable_broadcast()
        print("Warp synchronized input (broadcast) enabled for all panes.")

    if hosts:
        print(f"Launched {len(hosts)} SSH sessions in a new Warp window. "
              "Ensure Warp has Accessibility permissions.")


if __name__ == "__main__":
    main()
