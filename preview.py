from delivery import members, read_member
from dialects import profile
from csv_probe import parse_known
from intake_sink import inspect_records
from evidence import EvidenceStore


def preview_delivery(raw, source, directory):
    store = EvidenceStore(directory)
    digest = store.put(raw)
    inventory = list(members(raw))
    confirmed = profile(source)
    selected = next((member for member in inventory if member['name'].endswith('.csv') and member['path_safe']), None)
    if selected is None:
        raise ValueError('没有可预览的文本成员')
    content = read_member(raw, selected['ordinal'])
    result = inspect_records(parse_known(content, confirmed))
    store.record({'kind': 'preview', 'source': source, 'blob': digest,
                  'member': selected['ordinal'], 'profile_version': confirmed.version})
    return {'source': source, 'members': inventory, 'selected': selected, **result}
