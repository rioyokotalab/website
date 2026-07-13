#!/usr/bin/env python3
"""Add citation-evidenced ResearchMap metadata to mirrored achievement rows.

The visible citation remains the source of truth.  Each key below is a unique
literal shared by the English and Japanese pages; values are invisible HTML
data attributes consumed by ``researchmap-export.py``.  Reads and writes keep
the legacy CRLF bytes intact.
"""
import html
import os
import re


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    os.path.join(ROOT, 'en', 'achievements', 'index.html'),
    os.path.join(ROOT, 'jp', 'achievements', 'index.html'),
]

# Only values directly supported by the existing citations or an already
# present stable identifier belong here.  Unknown issue/page/location values
# intentionally remain absent.
UPDATES = {
    'On the Interplay Between Precision, Rank, Admissibility': {
        'data-title': ('On the Interplay Between Precision, Rank, Admissibility, '
                       'and Iterative Refinement for Hierarchical Low-Rank '
                       'Matrix Solvers'),
        'data-venue': 'ISC High Performance',
    },
    'Quantum turbulence coupled with externally driven normal-fluid': {
        'data-pages': '043601',
    },
    'Regularizing the Fast Multipole Method for use in Molecular Simulation': {
        'data-pages': '234113',
    },
    'Fast Multipole Method as a Matrix-Free Hierarchical Low-Rank': {
        'data-volume': '117',
    },
    'FMM と H^2(HSS) 行列のトレードオフについて': {
        'data-volume': '21',
        'data-number': '4',
        'data-pages': '3498-3501',
        'data-authors-ja': '横田理央',
        'data-authors-en': 'Rio Yokota',
    },
    '大規模境界要素法解析における分散並列 FMM の通信最適化': {
        'data-title': '大規模境界要素法解析における分散並列 FMM の通信最適化',
        'data-venue': 'シミュレーション',
        'data-volume': '35',
        'data-number': '3',
        'data-pages': '147-153',
        'data-authors-ja': '横田理央',
        'data-authors-en': 'Rio Yokota',
    },
    'Scaling FMM with data-driven OpenMP tasks on multicore architectures': {
        'data-volume': '9903',
    },
    'Communication complexity of the fast multipole method and its algebraic variants': {
        'data-pages': '63-84',
    },
    'FMM Tree Construction on GPUs': {
        'data-title': 'FMM Tree Construction on GPUs',
        'data-venue': 'Ensemble',
        'data-volume': '14',
        'data-number': '2',
        'data-pages': '85-89',
    },
    'N-body Simulation and FMM on the Large-scale GPU Cluster': {
        'data-volume': '15',
        'data-number': '4',
    },
    'The Study of Colliding Vortex Rings Using a Special-Purpose Computer': {
        'data-pages': '20080003',
    },
    '巨大行列とAI': {
        'data-book-title': '数学セミナー',
        'data-book-role': 'contributor',
        'data-volume': '59',
        'data-number': '2',
        'data-pages': '29-33',
        'data-authors-ja': '横田理央',
        'data-authors-en': 'Rio Yokota',
    },
    'スーパーコンピューティングコンテスト2019': {
        'data-book-title': '数学セミナー',
        'data-book-role': 'contributor',
        'data-volume': '59',
        'data-number': '1',
        'data-pages': '44-49',
        'data-authors-ja': '横田理央',
        'data-authors-en': 'Rio Yokota',
    },
    'N-body methods, High Performance Parallelism Pearls': {
        'data-book-title': 'High Performance Parallelism Pearls',
        'data-book-role': 'contributor',
    },
    'Treecode and fast multipole method for N-body simulation with CUDA': {
        'data-book-title': 'GPU Computing Gems Emerald Edition',
        'data-book-role': 'contributor',
    },
    'Rich Information is Affordable: A Systematic Performance Analysis': {
        'data-title': ('Rich Information is Affordable: A Systematic Performance '
                       'Analysis of Second-order Optimization Using K-FAC'),
        'data-venue': ('Proceedings of the 26th ACM SIGKDD International '
                       'Conference on Knowledge Discovery & Data Mining'),
    },
    'Sameer Deshmukh and Rio Yokota.': {
        'data-title': 'Distributed Memory Task-Based Block Low Rank Direct Solver',
        'data-venue': 'ISC High Performance 2020',
    },
    '(Really) Fast Macromolecular Electrostatics': {
        'data-title': ('(Really) Fast Macromolecular Electrostatics -- Fast '
                       'Algorithms, Open Software and Accelerated Computing'),
        'data-venue': 'ACS Division of Physical Chemistry 240th National Meeting',
    },
    'Privacy Preserving Visual SLAM': {
        'data-title': 'Privacy Preserving Visual SLAM',
        'data-venue': 'Proceedings of the European conference on computer vision (ECCV)',
    },
    'Performance Optimizations and Analysis of Distributed Deep Learning': {
        'data-number': '21',
    },
    'Communication Reducing Algorithms for Distributed Hierarchical N-Body': {
        'data-volume': '10266',
    },
    'Fork-Join and Data-Driven Execution Models on Multi-core Architectures': {
        'data-volume': '7905',
    },
    '画像超解像における学習データ構築の再考': {
        'data-title': '画像超解像における学習データ構築の再考',
        'data-venue': '第27回 画像の認識・理解シンポジウム (MIRU)',
    },
    'Ryo Nakamura, Ryu Tadokoro, Ryosuke Yamada': {
        'data-title': 'Scaling Backwards: Minimal Synthetic Pre-training?',
        'data-venue': 'European Conference on Computer Vision (ECCV)',
    },
    '片岡 裕雄、Scaling Backwards:': {
        'data-title': 'Scaling Backwards: Minimal Synthetic Pre-training?',
        'data-venue': '第27回 画像の認識・理解シンポジウム (MIRU)',
    },
    'PEZY-SC3sプロセッサを用いたFull-state量子回路シミュレーション': {
        'data-title': 'PEZY-SC3sプロセッサを用いたFull-state量子回路シミュレーション',
    },
    '低ランク近似行列によるCNNにおける畳み込み演算の最適化': {
        'data-volume': '2017-HPC-158',
        'data-number': '25',
    },
}

ALLOWED_REPLACEMENTS = {
    # Corrects the uncommitted first-run collision between the ECCV and MIRU
    # versions of the same paper title.
    ('Ryo Nakamura, Ryu Tadokoro, Ryosuke Yamada', 'data-venue',
     '第27回 画像の認識・理解シンポジウム (MIRU)'),
}


def update_page(path):
    with open(path, newline='', encoding='utf-8') as source:
        content = source.read()
    original = content
    for literal, attributes in UPDATES.items():
        lines = [line for line in content.splitlines(keepends=True)
                 if literal in line and re.search(r'<li\b', line, re.I)]
        if len(lines) != 1:
            raise ValueError('%s: expected one <li> for %r, found %d' %
                             (path, literal, len(lines)))
        line = lines[0]
        tag_match = re.search(r'<li\b[^>]*>', line, re.I)
        if not tag_match:
            raise ValueError('%s: opening <li> not found for %r' % (path, literal))
        tag = tag_match.group(0)
        original_tag = tag
        additions = []
        for name, value in attributes.items():
            existing = re.search(r'\b%s\s*=\s*(["\'])(.*?)\1' % re.escape(name),
                                 tag, re.I)
            if existing:
                if html.unescape(existing.group(2)) != value:
                    old_value = html.unescape(existing.group(2))
                    if (literal, name, old_value) not in ALLOWED_REPLACEMENTS:
                        raise ValueError('%s: conflicting %s for %r' %
                                         (path, name, literal))
                    escaped = html.escape(value, quote=True)
                    tag = (tag[:existing.start(2)] + escaped +
                           tag[existing.end(2):])
                continue
            additions.append(' %s="%s"' %
                             (name, html.escape(value, quote=True)))
        if additions or tag != original_tag:
            replacement = tag[:-1] + ''.join(additions) + '>'
            line = line[:tag_match.start()] + replacement + line[tag_match.end():]
            content = content.replace(lines[0], line, 1)
    if content != original:
        with open(path, 'w', newline='', encoding='utf-8') as target:
            target.write(content)


def opening_tags(path):
    with open(path, newline='', encoding='utf-8') as source:
        return re.findall(r'<li\b[^>]*>', source.read(), re.I)


def main():
    for page in PAGES:
        update_page(page)
    en_tags, jp_tags = (opening_tags(page) for page in PAGES)
    if en_tags != jp_tags:
        raise ValueError('EN/JP opening-tag parity failed after metadata update')
    print('updated %d metadata rows on two mirrored pages' % len(UPDATES))


if __name__ == '__main__':
    main()
