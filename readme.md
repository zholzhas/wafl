# WAFL framework for formal modelling Web Service Architectures

## Requirements
You need Maude installed on your system. The framework was developed using Maude 3.2.1. Other versions were not tested. The Maude executable will be denoted as `{MAUDE}`. 

## Usage
To use WAFL, run:
```
{MAUDE} wafl.maude
```

WAFL specifications are loaded directly by calling the `load` command:
```
load document-exchange.wafl
```

Examples of how WAFL can be used and features are provided in the examples.

## Examples
These are example used to test the capabilities of WAFL:
* orchestration.wafl
* choreography.wafl
* document-exchange.wafl
