# wcssh

A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default.

## Installation

### Homebrew (macOS & Linux)

First, tap the formula repository:

```sh
brew tap <your-username>/wcssh
```

Then, you can install `wcssh`:

```sh
brew install wcssh
```

## Usage

Here are some examples of how to use `wcssh`.

### Basic Usage

To open a new Warp window with SSH sessions to multiple hosts in separate panes with synchronized input:

```sh
wcssh user@host1.com user@host2.com user@host3.com
```

### Disabling Synchronized Input

Synchronized input is enabled by default. To disable it, use the `--no-broadcast` flag:

```sh
wcssh --no-broadcast user@host1.com user@host2.com user@host3.com
```

### From a file

You can also specify a file containing a list of hosts (one per line):

```sh
wcssh --hosts-file /path/to/your/hosts.txt
```
