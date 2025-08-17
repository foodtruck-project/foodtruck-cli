# bash completion for foodtruck

_foodtruck_completion() {
    local cur prev opts cmds
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    cmds="check setup completion --help --version"
    
    # Command-specific completions
    case "${prev}" in
        setup)
            # Setup command options
            opts="--api-repo --website-repo --target-dir --skip-api --skip-website --help"
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
        check)
            # Check command has no additional options
            COMPREPLY=( $(compgen -W "--help" -- "${cur}") )
            return 0
            ;;
        completion)
            # Completion command options
            opts="bash zsh powershell --help"
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
            return 0
            ;;
        --api-repo|--website-repo|--target-dir)
            # These options expect file/directory completion
            return 0
            ;;
        --skip-api|--skip-website)
            # Boolean flags
            COMPREPLY=( $(compgen -W "true false" -- "${cur}") )
            return 0
            ;;
        *)
            # Default completion for main commands
            COMPREPLY=( $(compgen -W "${cmds}" -- "${cur}") )
            return 0
            ;;
    esac
}

complete -F _foodtruck_completion foodtruck
