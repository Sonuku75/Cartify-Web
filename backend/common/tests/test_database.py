"""Automated test suite for PostgreSQL database integration, ORM transactions, and constraints."""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import connection, transaction
from django.test import TestCase, TransactionTestCase

User = get_user_model()


class PostgreSQLConnectionTests(TestCase):
    """Verifies PostgreSQL connection and configuration."""

    def test_database_engine_is_postgresql(self):
        """Ensure the active database engine is PostgreSQL."""
        engine = connection.settings_dict['ENGINE']
        self.assertEqual(engine, 'django.db.backends.postgresql')

    def test_database_connection_query(self):
        """Execute a raw query to verify direct PostgreSQL communication."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            self.assertEqual(row[0], 1)

    def test_relational_constraints_and_foreign_keys(self):
        """Verify relational integrity through foreign key relations."""
        user = User.objects.create_user(
            email='db_test@cartify.internal',
            password='SecurePassword123!',
        )
        group = Group.objects.create(name='TestGroup')
        user.groups.add(group)

        self.assertTrue(user.groups.filter(name='TestGroup').exists())
        self.assertEqual(group.user_set.count(), 1)


class PostgreSQLTransactionTests(TransactionTestCase):
    """Verifies database transaction atomicity and rollbacks."""

    def test_atomic_transaction_rollback(self):
        """Verify that an exception within an atomic block rolls back changes."""
        try:
            with transaction.atomic():
                User.objects.create_user(
                    email='rollback@cartify.internal',
                    password='Password123!',
                )
                raise ValueError("Simulated failure to trigger transaction rollback")
        except ValueError:
            pass

        self.assertFalse(User.objects.filter(email='rollback@cartify.internal').exists())

    def test_atomic_transaction_commit(self):
        """Verify that a successful atomic block commits changes to the database."""
        with transaction.atomic():
            user = User.objects.create_user(
                email='commit@cartify.internal',
                password='Password123!',
            )

        self.assertTrue(User.objects.filter(email='commit@cartify.internal').exists())
        user.delete()

