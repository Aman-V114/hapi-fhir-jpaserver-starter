#!/bin/bash

# Backup your data
echo "Backing up PostgreSQL data..."
pg_dumpall > backup.sql

# Stop PostgreSQL service
echo "Stopping PostgreSQL service..."
sudo systemctl stop postgresql

# Uninstall current PostgreSQL version
echo "Uninstalling current PostgreSQL version..."
sudo apt remove --purge postgresql* -y
sudo apt autoremove -y
sudo apt autoclean -y

# Add PostgreSQL APT repository
echo "Adding PostgreSQL APT repository..."
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

# Install PostgreSQL 14
echo "Installing PostgreSQL 14..."
sudo apt install postgresql-14 -y

# Start PostgreSQL service
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql

# Restore your data
echo "Restoring PostgreSQL data..."
psql -f backup.sql postgres

# Verify the installation
echo "Verifying PostgreSQL version..."
psql --version

echo "PostgreSQL downgrade to version 14 completed."