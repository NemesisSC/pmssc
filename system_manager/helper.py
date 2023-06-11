import uuid


def generate_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s" % (uuid.uuid4(), extension)
    return new_filename
