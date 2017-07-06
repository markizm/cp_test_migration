### Catchpoint Test Migration 

Endpoint: https://io.catchpoint.com/ui/help

Description: Script to migrate tests from/to different divisions

### Maintainer

Mark Magaling - magaling.markizm@gmail.com

### Requirements

Your server must have vault keys in /home/t/etc/vault_keys

### Usage

##### $ ./cp_migrate -t {testid} -d {destination div}

(test ids are obtained from the test settings, top of the page)

destination divisions:

"client" = client division

"nonprod" = non-prod division 

"dev" = dev division 

### Notes

Uses OAUTH2.0 framework for authentication 

Written in Python 2.7 

