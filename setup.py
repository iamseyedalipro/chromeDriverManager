from setuptools import setup, find_packages

# Read requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='chromeDriverManager',
    version='1.0.0',
    author='Seyed Ali Hosseini',
    author_email='iamseyedalipro@gmail.com',
    description='A class for managing the installation and updating of the chromedriver executable.',
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/chromeDriverManager',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    keywords='chromedriver automation selenium',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'chromedriver-manager=chromeDriverManager.chromedriver_manager:main',
        ],
    },
)
