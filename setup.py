from setuptools import setup, find_packages

setup(
    name='semantic-search',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'chromadb',
        'open-clip-torch',
        'Pillow',
        'pymupdf',
        'torch',
    ],
    entry_points={
        'console_scripts': [
            'sem-index=semantic_search.index:index',
            'sem-search=semantic_search.search:search',
        ],
    },
)