import argparse
import os

from outline.outline import Outline

outline = Outline(os.getenv("VPN_API_URL"))

print(outline.server.server_info())
