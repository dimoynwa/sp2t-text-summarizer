import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

__version__='0.0.1'

REPO_NAME='super-text-summary'
AUTHOR_USER_NAME='dimoynwa'
SRC_REPO='super_text_summary'
AUTHOR_EMAIL='dimodrangov@gmail.com'

setuptools.setup(
    name=SRC_REPO, 
    version=__version__, 
    author=AUTHOR_USER_NAME, 
    author_email=AUTHOR_EMAIL,
    description='Text summarization example project',
    long_description=description,
    long_description_content='text/markdown',
    url=f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    project_urls={
        "Bug Tracker": f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues'
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)