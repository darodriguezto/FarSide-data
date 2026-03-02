#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:18:02 2025

@author: daniel
"""


from sunpy.coordinates import frames
from astropy.coordinates import SkyCoord
import astropy.units as u
longitud = SkyCoord(-65 * u.deg, 0 * u.arcsec, frame=frames.HeliographicStonyhurst, obstime='2011-05-28', observer="earth")
Carrington= longitud.transform_to(frames.HeliographicCarrington)
lonCarrington = Carrington.lon.degree
print(lonCarrington)
