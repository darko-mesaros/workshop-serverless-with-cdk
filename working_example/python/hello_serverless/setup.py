import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="hello_serverless",
    version="0.1.2",

    description="CDK Project that produces a serverless application",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Darko Meszaros",

    package_dir={"": "hello_serverless"},
    packages=setuptools.find_packages(where="hello_serverless"),

    install_requires=[
        "aws-cdk.core==1.93.0",
        "aws-cdk.aws-lambda==1.93.0",
        "aws-cdk.aws-apigateway==1.93.0",
        "aws-cdk.aws-dynamodb==1.93.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
