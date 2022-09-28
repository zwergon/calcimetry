#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Calcimetry',
    version='0.1',
    description='module pour gérér les données Calcimetries de l andra',
    author='Jef Lecomte, John Armitage, Renaud Divies, Nina Khvoenkova',
    author_email='jean-francois.lecomte@ifpen.fr',
    url='https://tellus.gitlabpages.ifpen.fr/andra/ai.calcimetry/CalcimetryAPI.html',
    packages=['calcimetry', 'database', 'tests']
    )
