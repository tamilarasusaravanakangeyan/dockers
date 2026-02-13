# Data Persistence in Langflow

## ✅ Data is Now Persistent!

Your Langflow data is stored in a **bind mount** to your local drive, which means:

- ✅ **Data survives restarts** - `docker compose down` and `up` won't lose data
- ✅ **Data survives container recreation** - Even if you delete containers
- ✅ **Easy backup** - Just copy the `data` folder
- ✅ **Easy restore** - Copy the `data` folder back

## 📁 Data Location

All PostgreSQL data is stored in:
```
c:\Users\tamil\repo\tamilsmtp\dockers\langflow\data\postgres\
```

This directory contains:
- All your Langflow workflows
- User accounts and settings
- Flow execution history
- Component configurations

## 🔄 How It Works

The `docker-compose.yml` now uses a **bind mount** instead of a named volume:

```yaml
volumes:
  - ./data/postgres:/var/lib/postgresql/data
```

This maps the container's PostgreSQL data directory to your local `data/postgres` folder.

## 💾 Backup Your Data

### Manual Backup

Simply copy the entire `data` folder:

```bash
# Create a backup
xcopy /E /I data data_backup_2026-02-11

# Or compress it
tar -czf langflow_backup_2026-02-11.tar.gz data
```

### Automated Backup Script

Create a batch file `backup.bat`:

```batch
@echo off
set BACKUP_DIR=backups\%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%
mkdir %BACKUP_DIR%
xcopy /E /I data %BACKUP_DIR%\data
echo Backup completed to %BACKUP_DIR%
```

## 🔄 Restore Data

To restore from a backup:

1. **Stop Langflow**:
   ```bash
   docker compose down
   ```

2. **Replace the data folder**:
   ```bash
   # Delete current data
   rmdir /S /Q data
   
   # Restore from backup
   xcopy /E /I data_backup_2026-02-11 data
   ```

3. **Start Langflow**:
   ```bash
   docker compose up -d
   ```

## 🗑️ Clean Start (Delete All Data)

If you want to start fresh:

```bash
# Stop containers
docker compose down

# Delete data directory
rmdir /S /Q data

# Start fresh (data directory will be recreated)
docker compose up -d
```

## 📊 Check Data Size

To see how much space your data is using:

```bash
# Windows
dir data /s

# Or use PowerShell
Get-ChildItem -Path data -Recurse | Measure-Object -Property Length -Sum
```

## 🔒 Data Security

**Important Notes:**

1. **Backup Regularly** - Especially before major changes
2. **Protect Backups** - Store in a secure location
3. **Test Restores** - Verify backups work before you need them
4. **Version Control** - The `data` folder is in `.gitignore` (not committed to git)

## 🚀 Migration to Another Machine

To move Langflow to another machine:

1. **On old machine**:
   ```bash
   docker compose down
   # Copy the entire langflow folder including data/
   ```

2. **On new machine**:
   ```bash
   # Paste the langflow folder
   cd langflow
   docker compose up -d
   ```

All your workflows and settings will be preserved!

## ⚠️ Troubleshooting

### Data directory permissions error

If you get permission errors:

```bash
# Stop containers
docker compose down

# Fix permissions (run as administrator)
icacls data /grant Everyone:F /T

# Restart
docker compose up -d
```

### Database corruption

If the database gets corrupted:

1. Stop containers: `docker compose down`
2. Restore from backup (see above)
3. If no backup, delete `data` and start fresh

## 📝 Summary

- **Data Location**: `./data/postgres/`
- **Persistence**: ✅ Survives restarts and container recreation
- **Backup**: Copy the `data` folder
- **Restore**: Replace the `data` folder and restart
- **Clean Start**: Delete `data` folder and restart
