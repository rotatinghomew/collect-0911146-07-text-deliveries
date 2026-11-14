def inspect_records(records):
    accepted = []
    rejected = []
    for record in records:
        values = record['values']
        missing = [name for name in ['member_id', 'amount'] if not values.get(name)]
        if missing:
            rejected.append({'record': record['record'], 'reason': '缺少字段', 'fields': missing})
        else:
            accepted.append({'record': record['record'], **values})
    return {'accepted': accepted, 'rejected': rejected}
