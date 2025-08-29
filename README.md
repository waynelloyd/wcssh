# wcssh

A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default.

## Installation

### Homebrew (macOS)

Try the tap and install:

```sh
brew install waynelloyd/wcssh/wcssh
```

If that fails, follow the instructions below:

First, tap the formula repository:

```sh
brew tap waynelloyd/wcssh
```

Then, install the formula:

```sh
brew install wcssh
```

## Usage

### Command Line Arguments

```
wcssh [OPTIONS] [HOSTS...]
```

#### Options

- `--version` - Show version information and exit
- `--user`, `-u` - SSH username to use for all connections
- `--port`, `-p` - SSH port to use (default: 22)
- `--identity`, `-i` - Path to SSH private key file
- `--ssh-opts` - Additional raw SSH options string
- `--delay` - Base delay in seconds between UI actions (default: 0.1)
- `--no-broadcast` - Disable Warp synchronized input (broadcast) - enabled by default
- `--save-history` - Allow SSH commands to be saved to shell history (disabled by default)
- `--help`, `-h` - Show help message and exit

#### Arguments

- `HOSTS` - Target hosts for SSH connections (can be specified as arguments or piped from stdin). Hosts can be separated by spaces or commas, and the tool will intelligently parse them.

### Examples

#### Basic Usage

To open a new Warp window with SSH sessions to multiple hosts in separate panes with synchronized input:

```sh
wcssh user@host1.com user@host2.com user@host3.com
```

#### Flexible Host Separators

Hosts can be separated by spaces, commas, or a mix of both:

```sh
wcssh host1.com,host2.com host3.com
wcssh host1.com, host2.com, host3.com
```

#### Using SSH Options

Connect with a specific user, port, and SSH key:

```sh
wcssh --user myuser --port 2222 --identity ~/.ssh/my_key host1.com host2.com
```

#### Additional SSH Options

Pass additional SSH options:

```sh
wcssh --ssh-opts "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" host1.com host2.com
```

#### Disabling Synchronized Input

Synchronized input is enabled by default. To disable it, use the `--no-broadcast` flag:

```sh
wcssh --no-broadcast user@host1.com user@host2.com user@host3.com
```

#### From a File

You can also specify a file containing a list of hosts (one per line) and pipe it to `wcssh`:

```sh
cat /path/to/your/hosts.txt | wcssh
```

#### Custom Delay

Adjust the base delay for UI actions. Increase this value if commands are being missed or panes are not splitting correctly:

```sh
wcssh --delay 0.5 host1.com host2.com host3.com
```
