from dpns.scheduler.celery_tasks import app

# before you need stop celery worker
app.control.purge()
# app.control.discard_all()
