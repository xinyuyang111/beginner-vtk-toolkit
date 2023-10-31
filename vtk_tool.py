import vtk
import numpy as np


def show_points(poly_lst=[], points=[], poly_color_lst=[], add_axes=False):#(X, Y, Z)
    """
    show vtk.vtkPolyData, coordinate point, vtk.vtkPolyData's color, axis
    poly_lst:       list of vtk.vtkPolyData
    points:         list of coordinate point 
    poly_color_lst: list of vtk.vtkPolyData's color, The index is the same as that of poly_lst
    add_axes:       Whether to show coordinate axes
    """
    renderer = vtk.vtkRenderer()
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(1000, 1000, 1000)  # Set the total length of the axes in 3 dimensions(X, Y, Z)
    # Set the type of the shaft to a cylinder:0, line:1, or user defined geometry.
    axes.SetShaftType(0)
    axes.SetCylinderRadius(0.0002)
    axes.SetAxisLabels(0)
    if add_axes:
        renderer.AddActor(axes)
    for i, point in enumerate(points):

        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(point[0], point[1], point[2])
        sphere.SetRadius(1)
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())
        actor2 = vtk.vtkActor()
        actor2.SetMapper(sphereMapper)
        actor2.GetProperty().SetColor([255, 255, 255])
        actor2.GetProperty().SetRepresentationToSurface()
        renderer.AddActor(actor2)

    for i, poly in enumerate(poly_lst):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        if poly_color_lst:
            assert len(poly_lst) == len(poly_color_lst), "poly_lst and poly_color_lst should be the same length"
            for i in poly_color_lst:
                actor.GetProperty().SetColor(i)
        if i == 0:
            actor.GetProperty().SetOpacity(0.5)
        actor.GetMapper().ScalarVisibilityOn()
        renderer.AddActor(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindow.SetSize(1000, 1000)

    style = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor.SetInteractorStyle(style)

    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()

def stl_reader_polydata(path)->vtk.vtkPolyData:
    """
    path: .stl file path
    return vtk.vtkPolyData
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


def ply_reader_polydata(path)->vtk.vtkPolyData:
    reader = vtk.vtkPLYReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

def obj_reader_polydata(path)->vtk.vtkPolyData:
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


def stl_writer_polydata(poly, path):
    """
    poly: vtk.vtkPolyData
    path: .stl file path(xxx.stl)
    Save polydata to the path
    """
    writer = vtk.vtkSTLWriter()
    writer.SetInputData(poly)
    writer.SetFileName(path)
    writer.Write()
    

def point_projection_line(v, p):
    v_normalized = v / np.linalg.norm(v)
    return np.dot(p, v_normalized) * v_normalized

def point_dis(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5

def smooth_polydata(polydata, iter=100, factor=0.1):

    smooth_filter = vtk.vtkSmoothPolyDataFilter()
    smooth_filter.SetInputData(polydata)
    smooth_filter.SetNumberOfIterations(iter)  
    smooth_filter.SetRelaxationFactor(factor)  
    smooth_filter.Update()

    smoothed_polydata = smooth_filter.GetOutput()
    return smoothed_polydata
