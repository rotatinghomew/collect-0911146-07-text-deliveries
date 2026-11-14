import json
import tempfile
from fixtures import delivery
from preview import preview_delivery


def main():
    with tempfile.TemporaryDirectory() as directory:
        print(json.dumps(preview_delivery(delivery('west', multiline=True), 'west', directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
