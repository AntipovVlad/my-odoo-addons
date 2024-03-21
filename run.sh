docker compose down
docker volume rm odoo-main-extension_odoo_data odoo-main-extension_postgres_data
docker compose up -d
docker compose run odoo bash -c "odoo --init base --database crm --stop-after-init --db_host=postgres --db_user crm --db_password SecretPasswordDb
pip install bravado_core"
docker compose restart
