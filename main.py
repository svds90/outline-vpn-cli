import argparse
from modules.json_handler import JSONHandler
from outline.outline_api import OutlineVPN

cfg_handler = JSONHandler()
parser = argparse.ArgumentParser()
parser.add_argument("outline_api_url", type=str, help="Outline API URL")
