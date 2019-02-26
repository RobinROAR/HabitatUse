#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Functions on OGR Shapfile

from osgeo import ogr,osr
import os
import pandas as pd
import numpy




def create_shp_rec(xmin,xmax,ymin,ymax,name):
    '''
    Create a Rectangular shapfile via given coordinates
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    :return:
    '''
    # Create rec
    rec = ogr.Geometry(ogr.wkbLinearRing)
    rec.AddPoint(xmin, ymax)
    rec.AddPoint(xmax, ymax)
    rec.AddPoint(xmax, ymin)
    rec.AddPoint(xmin, ymin)
    #add linearRine to Polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(rec)
    # Save extent to a new Shapefile
    outShapefile = name
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    #set projection
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    # create a layer
    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer("rec_layer",srs, geom_type=ogr.wkbPolygon)
    # create ID field
    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    outLayer.CreateField(idField)
    # create feature set value
    featureDefn = outLayer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(poly)
    feature.SetField("id", 1)
    outLayer.CreateFeature(feature)
    feature = None
    # Save and close DataSource
    inDataSource = None
    outDataSource = None

def create_shp_points(points):
    '''
    create multipoints shapfile by given coordinates
    :param points:
    :return:
    '''
    print 'points number:',len(points)
    # Input data
    fieldName = 'points'
    fieldType = ogr.OFTString
    fieldValue = '1'
    outSHPfn = 'data/shp/points.shp'

    # Set projection
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    # Create the output shapefile
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outSHPfn):
        shpDriver.DeleteDataSource(outSHPfn)
    #create layer
    outDataSource = shpDriver.CreateDataSource(outSHPfn)
    outLayer = outDataSource.CreateLayer(outSHPfn, srs,geom_type=ogr.wkbMultiPoint)
    # create multipoint geometry
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    for i in points:
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(i[0], i[1])
        multipoint.AddGeometry(point)
        point = None

    # create a field
    idField = ogr.FieldDefn(fieldName, fieldType)
    outLayer.CreateField(idField)
    # Create the feature and set values
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(multipoint)
    outFeature.SetField(fieldName, fieldValue)
    outLayer.CreateFeature(outFeature)
    #close
    outFeature = None



def create_buffer(inputfn, outputBufferfn, bufferDist):
    '''
    create buffer areas on given points
    :param inputfn:
    :param outputBufferfn:
    :param bufferDist:
    :return:
    '''
    inputds = ogr.Open(inputfn)
    inputlyr = inputds.GetLayer()

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)

    # 设定投影
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    # 建立layer
    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, srs, geom_type=ogr.wkbPolygon)
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in inputlyr:
        ingeom = feature.GetGeometryRef()
        geomBuffer = ingeom.Buffer(bufferDist)

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geomBuffer)
        bufferlyr.CreateFeature(outFeature)
        outFeature = None
    print 'buffer finished'




#main
if __name__ == '__main__':

    #create a r
    #x_min, x_max, y_min, y_max =  96.6,102.4,38.8,34.2
    #x_min, x_max, y_min, y_max = 99.49,100.97,37.5,36.3
    #Small UD1
    #x_min, x_max, y_min, y_max = 99.478, 100.249, 37.190, 36.645
    #Small UD2
    x_min, x_max, y_min, y_max = 96.840, 98.809, 35.639,34.648
    #BIG ud
    #x_min, x_max, y_min, y_max = 96.800, 101.041, 37.353, 34.739
    name = './data/s2.shp'

    create_shp_rec(x_min,x_max,y_min,y_max,name)

    #create buffer
    # inputfn = 'data/shp/points.shp'
    # outputBufferfn = 'data/shp/testBuffer.shp'
    # bufferDist = 0.01
    # create_buffer(inputfn, outputBufferfn, bufferDist)