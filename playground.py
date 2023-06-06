from logger import log


log.i('just a basic info')
log.w('warning!!')
log.e('error without error')
arr = []
try:
    x = arr[1]
    x += 23
except Exception as e:
    log.e(exception=e)

