import io
import zipfile


def delivery(source='east', multiline=False, unsafe=False):
    buffer = io.BytesIO()
    delimiter = ';' if source == 'west' else ','
    text = delimiter.join(['member_id', 'amount', 'note']) + '\r\n'
    note = '"现场\n补充"' if multiline else '已确认'
    text += delimiter.join(['00017', '"1,250.00"', note]) + '\r\n'
    encoding = 'gb18030' if source == 'west' else 'utf-8-sig'
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('delivery/rows.csv', text.encode(encoding))
        archive.writestr('readme.txt', '数据来源：合作社演练'.encode())
        if unsafe:
            archive.writestr('../outside.csv', b'should not be extracted')
    return buffer.getvalue()
