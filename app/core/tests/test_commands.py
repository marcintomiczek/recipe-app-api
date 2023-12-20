"""Test custom Django management commands."""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, check):
        """Test waiting for database if database ready."""
        check.return_value = True

        call_command("wait_for_db")

        check.assert_called_once_with(databases=['default'])

    def test_wait_for_db_delay(self, check):
        """Test waiting for database when getting OperationalError."""
        check.side_effect = (
                [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        with patch("time.sleep"):
            call_command("wait_for_db")

        self.assertEquals(check.call_count, 6)
        check.assert_called_with(databases=['default'])
