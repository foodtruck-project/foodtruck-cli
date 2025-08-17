# PowerShell completion for foodtruck

Register-ArgumentCompleter -Native -CommandName foodtruck -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
    
    $completions = @(
        @{Command = "check"; Description = "Check dependencies"}
        @{Command = "setup"; Description = "Setup development environment"}
        @{Command = "completion"; Description = "Generate shell completion"}
        @{Command = "--help"; Description = "Show help"}
        @{Command = "--version"; Description = "Show version"}
    )
    
    $setupOptions = @(
        @{Option = "--api-repo"; Description = "API repository URL"}
        @{Option = "--website-repo"; Description = "Website repository URL"}
        @{Option = "--target-dir"; Description = "Target directory"}
        @{Option = "--skip-api"; Description = "Skip API setup"}
        @{Option = "--skip-website"; Description = "Skip website setup"}
        @{Option = "--help"; Description = "Show help"}
    )
    
    $completionOptions = @(
        @{Option = "bash"; Description = "Generate bash completion"}
        @{Option = "zsh"; Description = "Generate zsh completion"}
        @{Option = "powershell"; Description = "Generate PowerShell completion"}
        @{Option = "--help"; Description = "Show help"}
    )
    
    # Get the command being completed
    $command = $commandAst.CommandElements | Where-Object { $_.ToString() -ne "foodtruck" } | Select-Object -First 1
    
    if ($command) {
        switch ($command.ToString()) {
            "setup" {
                $setupOptions | Where-Object { $_.Option -like "$wordToComplete*" } | ForEach-Object {
                    [System.Management.Automation.CompletionResult]::new($_.Option, $_.Option, 'ParameterName', $_.Description)
                }
            }
            "check" {
                if ("--help" -like "$wordToComplete*") {
                    [System.Management.Automation.CompletionResult]::new("--help", "--help", 'ParameterName', "Show help")
                }
            }
            "completion" {
                $completionOptions | Where-Object { $_.Option -like "$wordToComplete*" } | ForEach-Object {
                    [System.Management.Automation.CompletionResult]::new($_.Option, $_.Option, 'ParameterName', $_.Description)
                }
            }
        }
    } else {
        # Main command completion
        $completions | Where-Object { $_.Command -like "$wordToComplete*" } | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_.Command, $_.Command, 'ParameterName', $_.Description)
        }
    }
}
