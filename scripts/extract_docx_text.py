#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml_bytes = zf.read('word/document.xml')
    root = ET.fromstring(xml_bytes)
    paragraphs = []
    for p in root.iter(W_NS + 'p'):
        texts = []
        for t in p.iter(W_NS + 't'):
            if t.text:
                texts.append(t.text)
        if texts:
            paragraphs.append(''.join(texts))
    text = '\n\n'.join(paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: extract_docx_text.py <path-to-docx>', file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    print(extract_docx_text(path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
