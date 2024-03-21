# Odoo main extension

## The repository

Repository for extending Odoo to MIEM by creating custom addons and custom docker-compose file. 

## Contributing

If you want to add business logic to Odoo you should 
create branch with you task's title, change main addon and create pull request.

## Using

### Deploy on server

1. `git clone https://git.miem.hse.ru/239/odoo/odoo-main-extension.git`
1. `docker build .`
1. `docker-compose up -d`
1. `docker-compose run odoo bash`
1. `odoo --init base --database crm --stop-after-init --db_host=postgres --db_user crm --db_password SecretPasswordDb`
1. `exit`
1. `docker-compose restart`

## License

Copyright (c) MIEM HSE. All rights reserved.

Licensed under the MIT license.
