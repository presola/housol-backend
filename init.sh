

python manage.py makemigrations userinfo
python manage.py migrate userinfo
python manage.py makemigrations timeseries
python manage.py migrate timeseries
python manage.py migrate --fake sessions zero
python manage.py showmigrations
python manage.py migrate --fake-initial

#python load.py
#python load-inflation.py
python load-prices.py
python manage.py loaddata sample_data.json
python manage.py loaddata inflation_data.json
python manage.py loaddata prices_data.json

echo Create first user
DJANGO_DB_NAME=default
DJANGO_SU_NAME=admin
DJANGO_SU_EMAIL=admin@test.com
DJANGO_SU_PASSWORD=testmeagain
if [ $DJANGO_SU_PASSWORD = "testmeagain" ]; then
        DJANGO_SU_PASSWORD=`head -c 10 /dev/random | base64`
        echo "${DJANGO_SU_PASSWORD}"
fi


python -c "import os;os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"HousingInsights.settings\");import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
   username='$DJANGO_SU_NAME', \
   email='$DJANGO_SU_EMAIL', \
   password='$DJANGO_SU_PASSWORD')"

echo "Success"

