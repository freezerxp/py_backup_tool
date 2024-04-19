"""
Запуск всех скриптов для создания резервных копий
Этот скрипт можно запустить, например, по расписанию из планировщика заданий
"""

import files_backup
import git_backup
import mysql_backup

files_backup.doBackup()
mysql_backup.doBackup()
git_backup.doBackup()