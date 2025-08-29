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

__version__ = "1.0.2"


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


def warp_cycle_panes_forward():
    # Cycle to the next pane (CMD+])
    run_applescript('tell application "System Events" to keystroke "]" using {command down}')


def warp_cycle_panes_backward():
    # Cycle to the previous pane (CMD+[)
    run_applescript('tell application "System Events" to keystroke "[" using {command down}')


def warp_type_and_enter(cmd: str):
    # It's safer to ensure Warp is active right before typing
    activate_warp()
    time.sleep(0.05)

    safe_cmd = cmd.replace("\\", "\\\\").replace('"', '\\"')
    applescript = f'tell application "System Events" to keystroke "{safe_cmd}"'
    run_applescript(applescript)
    time.sleep(0.02)
    run_applescript('tell application "System Events" to key code 36')  # Enter


def warp_enable_broadcast():
    # Enable Warp synchronized input using keyboard shortcut only
    activate_warp()
    time.sleep(0.1)
    
    # Use keyboard shortcut: Option + Command + I
    run_applescript('tell application "System Events" to keystroke "i" using {option down, command down}')


def get_all_hosts(cli_hosts: Optional[List[str]]) -> List[str]:
    """
    Reads hosts from stdin and CLI arguments, then parses and flattens them into a single list.
    Handles hosts separated by spaces, commas, or newlines.
    """
    all_inputs = cli_hosts or []

    # Read from stdin if available and add it to our list of inputs
    if not sys.stdin.isatty():
        all_inputs.append(sys.stdin.read())

    # Process all inputs together
    full_text = " ".join(all_inputs)
    # Replace commas and newlines with spaces for consistent splitting
    processed_text = full_text.replace(",", " ").replace("\n", " ")

    # Split by whitespace and filter out any empty strings that result
    return [host.strip() for host in processed_text.split() if host.strip()]


def create_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="wcssh — Warp multi-SSH launcher (macOS)")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("hosts", nargs="*", help="Target hosts")
    p.add_argument("--user", "-u", help="SSH username")
    p.add_argument("--port", "-p", default="22", help="SSH port (default 22)")
    p.add_argument("--identity", "-i", help="Path to SSH private key")
    p.add_argument("--ssh-opts", default="", help="Additional raw ssh options string")
    p.add_argument("--delay", type=float, default=0.1, help="Base delay in seconds between UI actions (default: 0.1)")
    p.add_argument(
        "--no-broadcast",
        action="store_true",
        help="Disable Warp synchronized input (broadcast) - enabled by default",
    )
    p.add_argument(
        "--save-history",
        action="store_true",
        help="Allow SSH commands to be saved to shell history (disabled by default)",
    )
    return p


def build_ssh_command(host: str, user: Optional[str], port: str, identity: Optional[str], ssh_opts: str, save_history: bool) -> str:
    target = f"{user}@{host}" if user else host
    ssh_parts = ["ssh"]
    if port:
        ssh_parts += ["-p", str(port)]
    if identity:
        ssh_parts += ["-i", identity]
    if ssh_opts:
        ssh_parts += shlex.split(ssh_opts)
    ssh_parts += [target]
    # shlex.join is the modern, correct way to join shell arguments (Python 3.8+)
    ssh_command = shlex.join(ssh_parts)

    return ssh_command if save_history else f"unset HISTFILE && {ssh_command}"


def main(argv: Optional[List[str]] = None):
    if sys.platform != "darwin":
        print("This script only runs on macOS.", file=sys.stderr)
        sys.exit(2)
    
    parser = create_arg_parser()
    args = parser.parse_args(argv)

    hosts = get_all_hosts(args.hosts)
    if not hosts:
        # argparse handles --version and --help automatically.
        # If we are here, it means no hosts were provided.
        print("Error: No hosts provided.", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    ssh_cmds = [build_ssh_command(h, args.user, args.port, args.identity, args.ssh_opts, args.save_history) for h in hosts]

    # Open a new Warp window
    warp_new_window()
    time.sleep(args.delay + 0.15)  # extra delay for window to appear
    activate_warp()
    time.sleep(0.05)

    # --- Phase 1: Create the pane layout ---
    # Create N-1 panes for the N hosts.
    num_hosts = len(ssh_cmds)
    for _ in range(num_hosts - 1):
        warp_split_right()
        time.sleep(args.delay + 0.1)  # Wait for the split to complete

    # --- Phase 2: Navigate and execute commands ---
    # After splitting, focus is on the last pane. Navigate back to the first pane.
    if num_hosts > 1:
        for _ in range(num_hosts - 1):
            warp_cycle_panes_backward()
            time.sleep(args.delay)

    # Now, iterate through the panes and type the commands
    for i, cmd in enumerate(ssh_cmds):
        # For all but the first host, we need to move to the next pane first
        if i > 0:
            warp_cycle_panes_forward()
            # This is a crucial delay to wait for the pane to become active before typing.
            # It's slightly longer to give the UI time to settle.
            time.sleep(args.delay + 0.05)

        warp_type_and_enter(cmd)
        # Small pause after typing to allow the ssh client to initialize before the next UI action
        time.sleep(args.delay + 0.1)

    # Enable broadcast by default unless disabled
    broadcast_enabled = False
    if not args.no_broadcast and len(ssh_cmds) > 1:
        time.sleep(0.5)  # Give time for all panes to be ready
        warp_enable_broadcast()
        broadcast_enabled = True

    print(f"\nLaunched {len(hosts)} SSH sessions in a new Warp window.")
    if broadcast_enabled:
        print("Warp synchronized input (broadcast) has been enabled.")
    print("Note: Ensure Warp has 'Accessibility' permissions in System Settings for full functionality.")


if __name__ == "__main__":
    main()
