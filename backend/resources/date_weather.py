#! /usr/bin/env python

from flask_restful import Api, Resource
from flask import request, g
import datetime
from sqlalchemy import and_, or_

class DateWeather(Resource):

    def get(self):
        """ Get the weather from start to end date interval
        ---
        parameters:
            - name: start
              in: body
              description: "weather record starting datetime"
              required: true
              type: string
              format: date-time
            - name: end
              in: body
              description: "weather record ending datetime"
              required: true
              type: string
              format: date-time

        definitions:
            DateWeather:
                type: object
                properties:
                    timestamp:
                        type: array
                        items:
                            type: string
                            format: date-time
                    temperature:
                        type: array
                        items:
                            type: number
                            format: float
                    pressure:
                        type: array
                        items:
                            type: numner
                            format: float
                    humidity:
                        type: array
                        items:
                            type: number
                            format: float
        responses:
            200:
                description: Response the weather data from database
                schema:
                    $ref: '#/definitions/DateWeather'
                examples:
                    timestamp: []
                    temperature: []
                    pressure: []
                    humidity: []
        """

        json_data = request.get_json(force=True) 
        # parse time with RFC3339 standard
        dt_parser = lambda s: datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f')
        start_time = dt_parser(json_data['start'])
        end_time = dt_parser(json_data['end'])

        wp_table = g.table_list["weather_param"]

        # filter the time between start and end
        cmd = g.session.filter(and_(wp_table.record_time > start, wp_table.record_time < end))
        record_time = []
        temperature = []
        humidity = []
        pressure = []

        for rec in cmd.all():
            record_time.append(rec.record_time)
            temperature.append(rec.temperature)
            humidity.append(rec.humidity)
            pressure.append(rec.pressure)

        return {'timestamp': record_time, 
                'temperature': temperature, 
                'pressure': pressure, 
                'humidity': humidity}, 200
