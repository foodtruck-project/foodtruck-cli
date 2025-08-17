"""
Tests for the completion command using carapace-bin
"""

import os
import platform
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest

from foodtruck_cli.commands.completion import (
    get_carapace_path,
    get_spec_file_path,
    save_carapace_spec,
    get_shell_setup_commands,
    get_carapace_config_dir,
    completion_command,
)


class TestGetCarapacePath:
    """Test carapace path detection"""

    def test_get_carapace_path_project_dir(self, tmp_path):
        """Test finding carapace in project directory"""
        # Create mock project structure
        project_dir = tmp_path / "foodtruck-cli"
        carapace_dir = project_dir / "carapace-bin"
        carapace_dir.mkdir(parents=True)
        
        if platform.system() == "Windows":
            carapace_exe = carapace_dir / "carapace.exe"
        else:
            carapace_exe = carapace_dir / "carapace"
        
        carapace_exe.write_text("mock executable")
        carapace_exe.chmod(0o755)
        
        with patch("foodtruck_cli.commands.completion.Path") as mock_path:
            mock_path.return_value.parent.parent.parent = project_dir
            result = get_carapace_path()
            
        assert result == carapace_exe

    @patch("shutil.which")
    def test_get_carapace_path_system(self, mock_which):
        """Test finding carapace in system PATH"""
        mock_which.return_value = "/usr/local/bin/carapace"
        
        # Mock the project directory to not exist by patching the exists method
        with patch("pathlib.Path.exists", return_value=False):
            result = get_carapace_path()
            
        # Should find carapace in system PATH
        assert result is not None
        assert str(result) == "/usr/local/bin/carapace"

    def test_get_carapace_path_not_found(self):
        """Test when carapace is not found"""
        with patch("foodtruck_cli.commands.completion.Path") as mock_path:
            mock_path.return_value.parent.parent.parent = Path("/nonexistent")
            with patch("shutil.which", return_value=None):
                result = get_carapace_path()
                
        assert result is None


class TestGetSpecFilePath:
    """Test spec file path detection"""

    def test_get_spec_file_path(self):
        """Test getting the spec file path"""
        result = get_spec_file_path()
        expected = Path(__file__).parent.parent / "foodtruck_cli" / "commands" / "complete.yaml"
        assert result == expected


class TestSaveCarapaceSpec:
    """Test saving carapace spec"""

    def test_save_carapace_spec_success(self, tmp_path):
        """Test successfully saving carapace spec"""
        spec_dir = tmp_path / "specs"
        source_spec = tmp_path / "complete.yaml"
        source_spec.write_text("mock yaml content")
        
        with patch("foodtruck_cli.commands.completion.get_spec_file_path", return_value=source_spec):
            result = save_carapace_spec(spec_dir)
            
        assert result == spec_dir / "foodtruck.yaml"
        assert (spec_dir / "foodtruck.yaml").exists()
        assert (spec_dir / "foodtruck.yaml").read_text() == "mock yaml content"

    def test_save_carapace_spec_source_not_found(self, tmp_path):
        """Test error when source spec file doesn't exist"""
        spec_dir = tmp_path / "specs"
        source_spec = tmp_path / "nonexistent.yaml"
        
        with patch("foodtruck_cli.commands.completion.get_spec_file_path", return_value=source_spec):
            with pytest.raises(FileNotFoundError, match="Spec file not found"):
                save_carapace_spec(spec_dir)


class TestGetShellSetupCommands:
    """Test shell setup command generation"""

    def test_get_shell_setup_commands_bash(self):
        """Test bash setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("bash", carapace_path)
        
        assert "export PATH=" in result
        assert "source <(" in result
        assert str(carapace_path) in result

    def test_get_shell_setup_commands_zsh(self):
        """Test zsh setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("zsh", carapace_path)
        
        assert "export PATH=" in result
        assert "export CARAPACE_BRIDGES=" in result
        assert "zstyle" in result
        assert "source <(" in result

    def test_get_shell_setup_commands_fish(self):
        """Test fish setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("fish", carapace_path)
        
        assert "set -Ux PATH" in result
        assert "set -Ux CARAPACE_BRIDGES" in result
        assert "source" in result

    def test_get_shell_setup_commands_powershell(self):
        """Test PowerShell setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("powershell", carapace_path)
        
        assert "$env:PATH" in result
        assert "$env:CARAPACE_BRIDGES" in result
        assert "Set-PSReadLineOption" in result
        assert "Out-String | Invoke-Expression" in result

    def test_get_shell_setup_commands_cmd(self):
        """Test CMD setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("cmd", carapace_path)
        
        assert "set PATH=" in result
        assert "CMD completion is limited" in result

    def test_get_shell_setup_commands_unsupported(self):
        """Test error for unsupported shell"""
        carapace_path = Path("/usr/local/bin/carapace")
        
        with pytest.raises(ValueError, match="Unsupported shell: invalid"):
            get_shell_setup_commands("invalid", carapace_path)

    @patch("platform.system")
    def test_get_shell_setup_commands_windows_paths(self, mock_system):
        """Test Windows path formatting"""
        mock_system.return_value = "Windows"
        carapace_path = Path("C:/Program Files/carapace/carapace.exe")
        result = get_shell_setup_commands("powershell", carapace_path)
        
        assert "C:\\Program Files\\carapace" in result
        assert "C:\\Program Files\\carapace\\carapace.exe" in result


class TestGetCarapaceConfigDir:
    """Test carapace config directory detection"""

    @patch("platform.system")
    def test_get_carapace_config_dir_windows(self, mock_system):
        """Test Windows config directory"""
        mock_system.return_value = "Windows"
        
        with patch.dict(os.environ, {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}):
            result = get_carapace_config_dir()
            
        expected = Path("C:\\Users\\test\\AppData\\Roaming") / "carapace" / "specs"
        assert result == expected

    @patch("platform.system")
    def test_get_carapace_config_dir_unix(self, mock_system):
        """Test Unix config directory"""
        mock_system.return_value = "Linux"
        
        result = get_carapace_config_dir()
        expected = Path.home() / ".config" / "carapace" / "specs"
        assert result == expected


class TestCompletionCommand:
    """Test completion command"""

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    @patch("foodtruck_cli.commands.completion.get_shell_setup_commands")
    @patch("foodtruck_cli.commands.completion.print_success")
    @patch("foodtruck_cli.commands.completion.print_warning")
    def test_completion_command_basic(self, mock_warning, mock_success, mock_setup, mock_carapace):
        """Test basic completion command"""
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        mock_setup.return_value = "mock setup commands"
        
        completion_command(shell="bash")
        
        mock_success.assert_called()
        mock_warning.assert_called_with("mock setup commands")

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    @patch("sys.exit")
    def test_completion_command_carapace_not_found(self, mock_exit, mock_carapace):
        """Test error when carapace is not found"""
        mock_carapace.return_value = None
        
        completion_command(shell="bash")
        
        mock_exit.assert_called_with(1)

    @patch("sys.exit")
    def test_completion_command_unsupported_shell(self, mock_exit):
        """Test error for unsupported shell"""
        completion_command(shell="invalid")
        
        mock_exit.assert_called_with(1)

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    @patch("foodtruck_cli.commands.completion.save_carapace_spec")
    @patch("foodtruck_cli.commands.completion.get_shell_setup_commands")
    @patch("foodtruck_cli.commands.completion.print_success")
    def test_completion_command_install(self, mock_success, mock_setup, mock_save, mock_carapace):
        """Test completion command with install flag"""
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        mock_save.return_value = Path("/tmp/spec.yaml")
        mock_setup.return_value = "mock setup commands"
        
        completion_command(shell="bash", install=True)
        
        mock_save.assert_called()
        assert mock_success.call_count >= 2  # At least 2 success messages

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    @patch("foodtruck_cli.commands.completion.get_shell_setup_commands")
    @patch("foodtruck_cli.commands.completion.print_success")
    def test_completion_command_output_file(self, mock_success, mock_setup, mock_carapace, tmp_path):
        """Test completion command with output file"""
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        mock_setup.return_value = "mock setup commands"
        output_file = tmp_path / "completion.sh"
        
        completion_command(shell="bash", output=output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "Food Truck CLI completion for bash" in content
        assert "mock setup commands" in content

    @patch("platform.system")
    @patch("os.environ")
    def test_completion_command_auto_detect_windows(self, mock_env, mock_system):
        """Test auto-detection on Windows"""
        mock_system.return_value = "Windows"
        mock_env.get.return_value = ""
        
        with patch("foodtruck_cli.commands.completion.get_carapace_path") as mock_carapace:
            mock_carapace.return_value = Path("/usr/local/bin/carapace")
            with patch("foodtruck_cli.commands.completion.get_shell_setup_commands") as mock_setup:
                mock_setup.return_value = "mock setup commands"
                with patch("foodtruck_cli.commands.completion.print_success"):
                    completion_command(shell="")
                
                # Should default to cmd on Windows
                mock_setup.assert_called_with("cmd", Path("/usr/local/bin/carapace"))

    @patch("platform.system")
    @patch("os.environ")
    def test_completion_command_auto_detect_unix(self, mock_env, mock_system):
        """Test auto-detection on Unix"""
        mock_system.return_value = "Linux"
        mock_env.get.return_value = "/bin/bash"
        
        with patch("foodtruck_cli.commands.completion.get_carapace_path") as mock_carapace:
            mock_carapace.return_value = Path("/usr/local/bin/carapace")
            with patch("foodtruck_cli.commands.completion.get_shell_setup_commands") as mock_setup:
                mock_setup.return_value = "mock setup commands"
                with patch("foodtruck_cli.commands.completion.print_success"):
                    completion_command(shell="")
                
                # Should default to bash on Unix
                mock_setup.assert_called_with("bash", Path("/usr/local/bin/carapace"))


class TestCompletionCommandIntegration:
    """Integration tests for completion command"""

    @pytest.mark.integration
    def test_completion_command_real_execution(self):
        """Test completion command with real execution (integration test)"""
        # This test requires carapace-bin to be installed
        # It's marked as integration test and can be skipped in CI
        pass

    @pytest.mark.integration
    def test_completion_command_windows_paths_real(self):
        """Test completion command with real Windows paths (integration test)"""
        # This test requires Windows environment
        # It's marked as integration test and can be skipped in CI
        pass
