def encodeMessage(msg, isBot=False):
    return {'sender':'Bot' if isBot else 'You',"message":msg }