def escape_string(msg):
    if msg is None:
        return None
    return msg.replace("'", "").replace('"', '').strip()

