#! /usr/bin/env python

from flask_restful import Api, Resource
from flask import request, g
import datetime
from sqlalchemy import and_, or_
import pytz

tzinfo = pytz.timezone('Asia/Shanghai')

class DateWeather(Resource):

    def post(self):
        """ Get the weather from start to end date interval
        ---
        requestBody:
            description: Define weather start datetine and end datetine
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/DateRange'
        definitions:
            DateRange:
                type: object
                properties:
                    start:
                      description: "weather record starting datetime"
                      required: true
                      type: string
                      format: date-time
                      example: "2020-06-19T17:27:09.018Z"
                    end:
                      description: "weather record ending datetime"
                      required: true
                      type: string
                      format: date-time
                      example: "2020-06-20T10:27:09.018Z"

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
                            type: number
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
        dt_parser = lambda s: datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f%z')
        start_time = dt_parser(json_data['start'])
        end_time = dt_parser(json_data['end'])

        wp_table = g.table_list["weather_param"]

        # filter the time between start and end
        cmd = g.session.query(wp_table).filter(and_(wp_table.record_time > start_time, wp_table.record_time < end_time))
        record_time = []
        temperature = []
        humidity = []
        pressure = []

        dt_formatter = lambda t: t.astimezone(tz=tzinfo).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        for rec in cmd.all():
            record_time.append(dt_formatter(rec.record_time))
            temperature.append(rec.temperature)
            humidity.append(rec.humidity)
            pressure.append(rec.pressure)

        return {'timestamp': record_time, 
                'temperature': temperature, 
                'pressure': pressure, 
                'humidity': humidity}, 200
