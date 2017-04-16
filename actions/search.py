def results(session):
    cuisine = session['entities'][0]['value']
    return "Searching for " + cuisine + " restaurant"