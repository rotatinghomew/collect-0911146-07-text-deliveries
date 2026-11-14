from pathlib import PurePosixPath
import hashlib
import io
import zipfile


def members(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for ordinal, info in enumerate(archive.infolist()):
            if info.is_dir():
                continue
            path = PurePosixPath(info.filename)
            yield {'ordinal': ordinal, 'name': info.filename, 'bytes': info.file_size,
                   'compressed_bytes': info.compress_size,
                   'path_safe': not path.is_absolute() and '..' not in path.parts,
                   'crc': info.CRC}


def read_member(raw, ordinal, limit=1048576):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        info = archive.infolist()[ordinal]
        if info.file_size > limit:
            raise ValueError('成员超过接收上限')
        with archive.open(info) as stream:
            content = stream.read(limit + 1)
        if len(content) > limit:
            raise ValueError('解码成员超过接收上限')
        return content
