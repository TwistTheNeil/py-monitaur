import uuid
import datetime

def create_new_uuid(name):
    return uuid.uuid3(
        uuid.NAMESPACE_DNS,
        name+datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    )