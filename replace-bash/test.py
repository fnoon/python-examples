#!/usr/bin/env python3

from unittest.mock import Mock, patch
import example

@patch('example.shutil')
@patch('example.Path')
def test_copy_ok(mock_path, mock_shutil):
    mock_result_path = Mock()
    mock_result_path.stat = Mock(return_value=Mock(st_mtime=1505056333.0))
    mock_path.return_value.stat = Mock(return_value=Mock(st_mtime=1505056332.0))

    example.copy_to_current(mock_path)

    mock_shutil.copy2.assert_called_once_with(
        str(mock_result_path), str(mock_path.return_value))
