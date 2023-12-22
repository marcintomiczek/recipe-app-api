"""Test custom Django management commands."""
from unittest.mock import patch, DEFAULT

from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch.object(connection, "ensure_connection")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, ensure_connection):
        """Test waiting for database if database ready."""
        call_command("wait_for_db")

        ensure_connection.assert_called_once()

    def test_wait_for_db_delay(self, ensure_connection):
        """Test waiting for database when getting OperationalError."""
        ensure_connection.side_effect = (
            [OperationalError] * 3 + [DEFAULT]
        )

        with patch("time.sleep"):
            call_command("wait_for_db")

        self.assertEqual(ensure_connection.call_count, 4)
        ensure_connection.assert_called()
