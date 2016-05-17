#!/usr/bin/python3
from xml.etree import cElementTree
from .features import FeatureCollection
from geojson import Feature, MultiLineString
import geojson
from osgeo import ogr

class SampleStreets(object):
	__title = 'Ulice'

	def __init__(self, dbFile):
		self.tree = cElementTree.ElementTree(file=dbFile)

	def all_streets(self):
		streets = []

		for street in self.tree.findall(".//Ulice"):
			street_id = int(street.get('kod'))
			segments = []

			for segment in street.findall('Geometrie/PosList'):
				coords = segment.text.split()
				points = []

				for i in range(0, len(coords), 2):
					points.append((float(coords[i]), float(coords[i + 1])))

				segments.append(points)

			mls = MultiLineString(segments)
			geom = ogr.CreateGeometryFromJson(geojson.dumps(mls))
			street_feature = Feature(geometry=mls, properties={'name': street.find('Nazev').text, 'length': geom.Length()}, id=street_id)
			streets.append(street_feature)

		return FeatureCollection(self.__title, streets)
