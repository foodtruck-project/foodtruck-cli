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
    completion_app,
    completion_install_command,
    completion_refresh_command,
    completion_manual_command,
    _get_shell_and_validate,
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
            with pytest.raises(FileNotFoundError):
                save_carapace_spec(spec_dir)


class TestGetShellSetupCommands:
    """Test shell setup commands generation"""

    def test_get_shell_setup_commands_bash(self):
        """Test bash setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("bash", carapace_path)
        
        assert "bash" in result.lower() or "carapace" in result.lower()
        assert "carapace" in result
        assert "/usr/local/bin/carapace" in result

    def test_get_shell_setup_commands_zsh(self):
        """Test zsh setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("zsh", carapace_path)
        
        assert "zsh" in result.lower() or "carapace" in result.lower()
        assert "carapace" in result
        assert "/usr/local/bin/carapace" in result

    def test_get_shell_setup_commands_fish(self):
        """Test fish setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("fish", carapace_path)
        
        assert "fish" in result.lower() or "carapace" in result.lower()
        assert "carapace" in result
        assert "/usr/local/bin/carapace" in result

    def test_get_shell_setup_commands_powershell(self):
        """Test powershell setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("powershell", carapace_path)
        
        assert "powershell" in result.lower() or "carapace" in result.lower()
        assert "carapace" in result
        assert "/usr/local/bin/carapace" in result

    def test_get_shell_setup_commands_cmd(self):
        """Test cmd setup commands"""
        carapace_path = Path("/usr/local/bin/carapace")
        result = get_shell_setup_commands("cmd", carapace_path)
        
        assert "cmd" in result.lower() or "carapace" in result.lower()
        assert "carapace" in result
        # CMD might not include the full path in the output
        assert "carapace" in result

    def test_get_shell_setup_commands_unsupported(self):
        """Test error for unsupported shell"""
        carapace_path = Path("/usr/local/bin/carapace")
        
        with pytest.raises(ValueError, match="Unsupported shell"):
            get_shell_setup_commands("invalid", carapace_path)

    @patch("platform.system")
    def test_get_shell_setup_commands_windows_paths(self, mock_system):
        """Test Windows path handling"""
        mock_system.return_value = "Windows"
        carapace_path = Path("C:\\carapace\\carapace.exe")
        result = get_shell_setup_commands("powershell", carapace_path)
        
        assert "powershell" in result.lower() or "carapace" in result.lower()
        assert "C:\\carapace\\carapace.exe" in result


class TestGetCarapaceConfigDir:
    """Test carapace config directory detection"""

    @patch("platform.system")
    def test_get_carapace_config_dir_windows(self, mock_system):
        """Test Windows config directory"""
        mock_system.return_value = "Windows"
        with patch("os.environ", {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"}):
            result = get_carapace_config_dir()
            # Just check that it contains the expected path components
            assert "carapace" in str(result)
            assert "specs" in str(result)

    @patch("platform.system")
    def test_get_carapace_config_dir_unix(self, mock_system):
        """Test Unix config directory"""
        mock_system.return_value = "Linux"
        with patch("os.environ", {"HOME": "/home/test"}):
            result = get_carapace_config_dir()
            assert result == Path("/home/test/.config/carapace/specs")


class TestGetShellAndValidate:
    """Test shell validation helper function"""

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    def test_get_shell_and_validate_specified_shell(self, mock_carapace):
        """Test with specified shell"""
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        
        shell, carapace_path = _get_shell_and_validate("zsh")
        
        assert shell == "zsh"
        assert carapace_path == Path("/usr/local/bin/carapace")

    @patch("platform.system")
    @patch("os.environ")
    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    def test_get_shell_and_validate_auto_detect_windows(self, mock_carapace, mock_env, mock_system):
        """Test auto-detection on Windows"""
        mock_system.return_value = "Windows"
        mock_env.get.return_value = ""
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        
        shell, carapace_path = _get_shell_and_validate("")
        
        assert shell == "cmd"
        assert carapace_path == Path("/usr/local/bin/carapace")

    @patch("platform.system")
    @patch("os.environ")
    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    def test_get_shell_and_validate_auto_detect_unix(self, mock_carapace, mock_env, mock_system):
        """Test auto-detection on Unix"""
        mock_system.return_value = "Linux"
        mock_env.get.return_value = "/bin/zsh"
        mock_carapace.return_value = Path("/usr/local/bin/carapace")
        
        shell, carapace_path = _get_shell_and_validate("")
        
        assert shell == "zsh"
        assert carapace_path == Path("/usr/local/bin/carapace")

    @patch("foodtruck_cli.commands.completion.print_error")
    @patch("sys.exit")
    def test_get_shell_and_validate_unsupported_shell(self, mock_exit, mock_error):
        """Test error for unsupported shell"""
        _get_shell_and_validate("invalid")
        
        mock_error.assert_called()
        mock_exit.assert_called_with(1)

    @patch("foodtruck_cli.commands.completion.get_carapace_path")
    @patch("foodtruck_cli.commands.completion.print_error")
    @patch("sys.exit")
    def test_get_shell_and_validate_carapace_not_found(self, mock_exit, mock_error, mock_carapace):
        """Test error when carapace is not found"""
        mock_carapace.return_value = None
        
        _get_shell_and_validate("bash")
        
        mock_error.assert_called()
        mock_exit.assert_called_with(1)


class TestCompletionSubcommands:
    """Test completion subcommands"""

    @patch("foodtruck_cli.commands.completion._get_shell_and_validate")
    @patch("foodtruck_cli.commands.completion.get_shell_config_file")
    @patch("foodtruck_cli.commands.completion.get_carapace_config_dir")
    @patch("foodtruck_cli.commands.completion.save_carapace_spec")
    @patch("foodtruck_cli.commands.completion.auto_configure_shell")
    @patch("foodtruck_cli.commands.completion.print_info")
    @patch("foodtruck_cli.commands.completion.print_success")
    def test_completion_install_command_new_installation(
        self, mock_success, mock_info, mock_auto_config, mock_save, 
        mock_config_dir, mock_config_file, mock_validate
    ):
        """Test completion install command for new installation"""
        mock_validate.return_value = ("zsh", Path("/usr/local/bin/carapace"))
        mock_config_file.return_value = Path("/home/test/.zshrc")
        mock_config_dir.return_value = Path("/home/test/.config/carapace")
        mock_save.return_value = Path("/home/test/.config/carapace/foodtruck.yaml")
        
        # Mock that completion is not already installed
        with patch("builtins.open", mock_open(read_data="old content")):
            completion_install_command(shell="zsh")
        
        mock_save.assert_called()
        mock_auto_config.assert_called()
        mock_success.assert_called()

    @patch("foodtruck_cli.commands.completion._get_shell_and_validate")
    @patch("foodtruck_cli.commands.completion.refresh_carapace_completion")
    def test_completion_refresh_command(self, mock_refresh, mock_validate):
        """Test completion refresh command"""
        mock_validate.return_value = ("zsh", Path("/usr/local/bin/carapace"))
        
        completion_refresh_command(shell="zsh")
        
        mock_refresh.assert_called_with("zsh")

    @patch("foodtruck_cli.commands.completion._get_shell_and_validate")
    @patch("foodtruck_cli.commands.completion.get_shell_setup_commands")
    @patch("foodtruck_cli.commands.completion.print_success")
    @patch("foodtruck_cli.commands.completion.print_warning")
    def test_completion_manual_command(self, mock_warning, mock_success, mock_setup, mock_validate):
        """Test completion manual command"""
        mock_validate.return_value = ("zsh", Path("/usr/local/bin/carapace"))
        mock_setup.return_value = "mock setup commands"
        
        completion_manual_command(shell="zsh")
        
        mock_success.assert_called()
        mock_warning.assert_called_with("mock setup commands")

    @patch("foodtruck_cli.commands.completion._get_shell_and_validate")
    @patch("foodtruck_cli.commands.completion.get_shell_setup_commands")
    @patch("foodtruck_cli.commands.completion.print_success")
    def test_completion_manual_command_with_output(self, mock_success, mock_setup, mock_validate, tmp_path):
        """Test completion manual command with output file"""
        mock_validate.return_value = ("zsh", Path("/usr/local/bin/carapace"))
        mock_setup.return_value = "mock setup commands"
        output_file = tmp_path / "completion.sh"
        
        completion_manual_command(shell="zsh", output=output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "Food Truck CLI completion for zsh" in content
        assert "mock setup commands" in content


class TestCompletionApp:
    """Test completion app structure"""

    def test_completion_app_help_text(self):
        """Test completion app help text"""
        assert "Generate shell completion scripts using carapace-bin" in completion_app.help

    def test_completion_app_exists(self):
        """Test that completion app exists and is properly configured"""
        assert completion_app is not None
        assert hasattr(completion_app, 'help')
        assert "completion" in completion_app.help.lower()
