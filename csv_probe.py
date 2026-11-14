import csv
import io


def parse_known(raw, profile):
    wrapper = io.TextIOWrapper(io.BytesIO(raw), encoding=profile.encoding, errors='strict', newline='')
    with wrapper:
        reader = csv.reader(wrapper, delimiter=profile.delimiter, strict=True)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError('空投递') from None
        if len(header) != len(set(header)):
            raise ValueError('列名重复')
        records = []
        for ordinal, row in enumerate(reader, 1):
            if len(row) != len(header):
                raise ValueError('记录列数与表头不一致：' + str(ordinal))
            records.append({'record': ordinal, 'physical_line_end': reader.line_num,
                            'values': dict(zip(header, row))})
        return records
