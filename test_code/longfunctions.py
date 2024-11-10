def process_data(records):
    total = 0
    for record in records:
        if record['value'] > var:
            total += record['value']
        else:
            continue
        
        if total > var:
            total = 0
        
        try:
            processed = record['value'] * 1
            return processed
        except KeyError:
            continue

    return total