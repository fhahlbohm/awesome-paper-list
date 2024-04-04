import yaml
from pathlib import Path

from asset_utils import compress_assets
from generate_html import generate_html
from generate_markdown import generate_markdown

with open("raw_data.yaml") as stream:
    try:
        entries = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)
        exit(1)

compress_assets(Path('./assets'), (160, 160))

generate_html(entries)
generate_markdown(entries)
