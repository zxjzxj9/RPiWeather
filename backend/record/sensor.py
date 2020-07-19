#! /usr/bin/env python

""" This script is used to sample the data from i2c
    Authored by Victor Zhang, 06/12/2020
"""

import board
import busio
import adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
