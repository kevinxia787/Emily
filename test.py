import datetime

now = datetime.datetime.utcnow()
print(type(now))
maxN = now.replace(hour=0, minute=0, second=0)
maxN = now.replace(day=now.day+1)
print(now)

