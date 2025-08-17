# Shell Completion Scripts

This directory contains shell completion scripts for the Food Truck CLI.

## Available Scripts

- `foodtruck.bash` - Bash completion script
- `_foodtruck` - Zsh completion script  
- `foodtruck.ps1` - PowerShell completion script

## Installation

### Automatic Installation

The completion scripts are automatically installed when you run the installation script:

```bash
python3 install.py
```

### Manual Installation

#### Bash

1. Copy the completion script to the bash completion directory:
   ```bash
   sudo cp completions/foodtruck.bash /etc/bash_completion.d/foodtruck
   ```

2. Or source it in your `.bashrc`:
   ```bash
   echo "source $(pwd)/completions/foodtruck.bash" >> ~/.bashrc
   ```

#### Zsh

1. Create the completions directory:
   ```bash
   mkdir -p ~/.zsh/completions
   ```

2. Copy the completion script:
   ```bash
   cp completions/_foodtruck ~/.zsh/completions/
   ```

3. Add to your `.zshrc`:
   ```bash
   echo "fpath=(~/.zsh/completions $fpath)" >> ~/.zshrc
   echo "autoload -U compinit && compinit" >> ~/.zshrc
   ```

#### PowerShell

1. Copy the completion script to your PowerShell profile:
   ```powershell
   Copy-Item completions/foodtruck.ps1 $PROFILE
   ```

2. Or source it in your profile:
   ```powershell
   Add-Content $PROFILE ". '$(Get-Location)\completions\foodtruck.ps1'"
   ```

## Using the CLI Completion Command

You can also use the built-in completion command:

```bash
# Generate completion scripts
foodtruck completion

# Install completion for a specific shell
foodtruck completion bash --install
foodtruck completion zsh --install
foodtruck completion powershell --install

# Generate and save to a specific file
foodtruck completion bash --output ~/.local/share/bash-completion/completions/foodtruck
```

## Features

The completion scripts provide:

- Command completion (check, setup, completion)
- Option completion for each command
- File/directory completion for path arguments
- Boolean flag completion
- Help text for options

## Testing

After installation, restart your shell or reload your profile, then test completion:

```bash
# Bash/Zsh
foodtruck <TAB>

# PowerShell
foodtruck <TAB>
```
