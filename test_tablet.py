import unittest
from unittest.mock import patch, mock_open

from tablet_mode import check_state, rotate_right

class TestTabletMode(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="0\n")
    def test_check_state_enabled(self, mock_file):
        result = check_state()
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open, read_data="1\n")
    def test_check_state_disabled(self, mock_file):
        result = check_state()
        self.assertFalse(result)
    
    @patch("tablet_mode.get_current_rotation")
    @patch("tablet_mode.subprocess.run")
    def test_rotate_right(self, mock_subproc, mock_get_rotation):
        mock_get_rotation.return_value = "normal"
        rotate_right()
        args, kwargs = mock_subproc.call_args
        command_list = args[0]
        self.assertIn("right", command_list)

if __name__ == "__main__":
    unittest.main()