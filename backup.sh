#!/bin/bash

# vars
BACKUP_DIR=~/synced/odoo_backups
ODOO_DATABASE=crm
ADMIN_PASSWORD=SecretPasswordDb

# create a backup directory
mkdir -p ${BACKUP_DIR}

# create a backup
curl -X POST \
    -F "master_pwd=${ADMIN_PASSWORD}" \
    -F "name=${ODOO_DATABASE}" \
    -F "backup_format=zip" \
    -o "${BACKUP_DIR}/${ODOO_DATABASE}.$(date +%F).zip" \
    http://localhost:8069/web/database/backup


# delete old backups
find ${BACKUP_DIR} -type f -mtime +7 -name "${ODOO_DATABASE}.*.zip" -delete

yandex-disk -d synced sync
