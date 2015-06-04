# survey
A very simple survey tools for logged-in users

**Big issue** : Need to be patched to remove django DEBUG on production !

# Build
    docker build --rm -t templateName .

# Prepare
    dockercmd='docker run --rm -i -t -e "DJANGO_SECRET_KEY="A_SECRET_KEY" -v "/docker/data/survey/db/:/data/proj/db" -v "/docker/data/survey:/data/proj/survey" -P -t templateName'

#Init
    $dockercmd python manage.py migrate
    $dockercmd python manage.py createsuperuser

# Upgrade
    $dockercmd python manage.py migrate

# Run
    $dockercmd
