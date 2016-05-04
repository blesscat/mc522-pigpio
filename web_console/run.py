import os


if not os.path.exists('/tmp/app.db'):
    os.system('cp -f app/app.db /tmp/app.db')

from app import app as application

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
