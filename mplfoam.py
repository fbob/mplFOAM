# encoding: utf-8
# mplFOAM module
# some useful functions to import, plot OpenFoam data with matplotlib

import os
import numpy as np

try: paraview.simple
except: from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

from vtk.util import numpy_support as npvtk

def read_openfoam_case(verbose=False,**kwargs):
    """
    Read the OpenFOAM case

    Parameters
    ----------
    directory : str, optional
                Directory path of the OpenFOAM case

    filename : str, optional
                Filename of the .OpenfOAM case for Paraview

    mesh_parts : list of str
                List of the different parts of the mesh to be loaded

    volume_fields : list of str
                List of the different fields to be loaded

    times : list of str
            List of the different timestep to be loaded

    Return
    ------
    openfoam_case_merged : paraview object
    """

    # Create the OpenFOAM file case
    if kwargs.get('directory') is None:
        directory = os.getcwd().split('/')[-1]

    if kwargs.get('filename') is None:
        filename = directory +'.OpenFOAM'

    case_file = open(filename, 'w')
    case_file.close()

    # Define the OpenFOAM data source
    openfoam_case = OpenDataFile(filename)

    # Import all the mesh parts if none are specified
    if kwargs.get('mesh_parts') is None:
        mesh_parts = openfoam_case.MeshParts.Available
    openfoam_case.MeshParts = mesh_parts

    # Import all the volume fields if none are specified
    if kwargs.get('volume_fields') is None:
        volume_fields = openfoam_case.VolumeFields.Available
    openfoam_case.VolumeFields = volume_fields

    # Read the specified time steps
    if kwargs.get('times') is None:
        # Get the latest timestep if none is specified
        openfoam_case.TimestepValues = openfoam_case.TimestepValues[-1]
    else:
        openfoam_case.TimestepValues = times

    # Print some basic informations on the loaded case
    if verbose:
        print "Case filename: ", filename
        print "Mesh parts: ", mesh_parts
        print "Volume fields: ", volume_fields
        print "Timestep values: ", openfoam_case.TimestepValues

    openfoam_case_merged = MergeBlocks(openfoam_case)
    openfoam_data = servermanager.Fetch(openfoam_case_merged)

    return openfoam_case_merged

def extractDataInPatch(case, verbose=False):
    "Extract the data from a patch and"

    # Select the active source
    #SetActiveSource(case)

    # Define the data
    Tetrahedralize1 = Tetrahedralize()
    data = servermanager.Fetch(Tetrahedralize1)

    # Define the number of points, cells and arrays
    nb_points = case.GetNumberOfPoints()
    nb_cells = case.GetNumberOfCells()
    nb_arrays = case.GetPointData().GetNumberOfArrays()

    # Get Paraview's own triangulation
    #cells = data.GetPolys()
    #triangles = cells.GetData()
    #nb_triangles = triangles.GetNumberOfTuples()/4

    nb_triangles = nb_cells
    tri = np.zeros((nb_triangles, 3))

    #for i in xrange(0, nb_triangles):
    #     tri[i, 0] = triangles.GetTuple(4*i + 1)[0]
    #     tri[i, 1] = triangles.GetTuple(4*i + 2)[0]
    #     tri[i, 2] = triangles.GetTuple(4*i + 3)[0]

    # Display some informations on the slice
    if verbose:

        #print 'Patch name :', patchName
        print "Number of cells:",nb_cells
        print "Number of triangles:",nb_triangles
        print "Number of points:",nb_points
        print "Number of arrays:",nb_arrays

        for i in range(nb_arrays):
            print 'Array [',i,'] name:', case.GetPointData().GetArrayName(i)

    # Put the points coordinates in x, y and z arrays
    x=[]
    y=[]
    z=[]
    #points=zeros((nb_points,3))

    for i in range(nb_points):
        coord = case.GetPoint(i)
        xx, yy, zz = coord[:3]
        x.append(xx)
        y.append(yy)
        z.append(zz)

        #points[i,0] = xx
        #points[i,1] = yy
        #points[i,2] = zz

    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    #print 'Points',points

    # Define the velocity components U=(u,v,w)
    U = npvtk.vtk_to_numpy(case.GetPointData().GetArray('U'))
    u = U[:,0]
    v = U[:,1]
    w = U[:,2]

    # Define the cinematique pressure p => p/\rho
    p = npvtk.vtk_to_numpy(case.GetPointData().GetArray('p'))

    # Return the values extracted from the slice
    return x,y,z,u,v,w,p,tri

def extract_plane(case, slice_origin=[0,0,0],slice_normal=[0,0,1], verbose=False):
    """
    Extract Paraview slice object from OpenFOAM case `case`

    Parameters
    ----------
    case : Paraview object
            OpenFOAM case

    slice_origin : list of float
                    Slice point origin [x, y, z] in cartesian coordinates

    slice_normal : list of float
                    Slice point normal [nx, ny, nz] in cartesian coordinates

    Return
    ------
    plane_data: paraview slice object

    """
    # Select the active source
    SetActiveSource(case)

    # Define the plane
    Slice1 = Slice(SliceType="Plane")
    Slice1.SliceType = 'Plane'
    Slice1.SliceType.Origin = slice_origin
    Slice1.SliceType.Normal = slice_normal
    #Slice1.UpdatePipeline()

    plane_data = servermanager.Fetch(Slice1)

    # Define the number of points, cells and arrays
    nb_points = plane_data.GetNumberOfPoints()
    nb_cells = plane_data.GetNumberOfCells()
    nb_arrays = plane_data.GetPointData().GetNumberOfArrays()

    # Display some informations on the slice
    if verbose:
        print 'Slice origin:', slice_origin
        print 'Slice normal:', slice_normal
        print "Number of cells:", nb_cells
        print "Number of triangles:", nb_triangles
        print "Number of points:", nb_points
        print "Number of arrays:", nb_arrays

        for i in range(nb_arrays):
            print 'Array [',i,'] name:', plane_data.GetPointData().GetArrayName(i)

    return plane_data

def extract_plane_triangulation(plane_data, verbose=False):
    """Extract the triangulation of the plane"""

    # Get Paraview's own triangulation
    cells = plane_data.GetPolys()
    triangles = cells.GetData()
    nb_triangles = triangles.GetNumberOfTuples()/4

    tri = np.zeros((nb_triangles, 3))

    for i in xrange(0, nb_triangles):
        tri[i, 0] = triangles.GetTuple(4*i + 1)[0]
        tri[i, 1] = triangles.GetTuple(4*i + 2)[0]
        tri[i, 2] = triangles.GetTuple(4*i + 3)[0]

    # Display some informations on the triangulation
    if verbose:
        print "Number of triangles:", nb_triangles

    # Return the triangulation of the plane
    return tri, triangles

def extract_plane_points(plane_data, verbose=False):
    """Extract the points of the plane"""

    # Get the number of points
    nb_points = plane_data.GetNumberOfPoints()

    # Put the points coordinates in x, y and z arrays
    x = []
    y = []
    z = []

    for i in range(nb_points):
        coord = plane_data.GetPoint(i)
        xx, yy, zz = coord[:3]
        x.append(xx)
        y.append(yy)
        z.append(zz)

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    # Display some informations on the triangulation points
    if verbose:
        print "Number of points:", nb_points
        print "xrange: [%5.3f, %5.3f]" %(x.min(), x.max())
        print "yrange: [%5.3f, %5.3f]" %(y.min(), y.max())
        print "zrange: [%5.3f, %5.3f]" %(z.min(), z.max())

    # Return the cartesian coordinates of the triangulation points
    return x,y,z

def extract_plane_vector_field(plane_data, field_name, verbose=False):
    """Extract the vector field components in the plane"""

    # Define the velocity components U=(u,v,w)
    U = npvtk.vtk_to_numpy(plane_data.GetPointData().GetArray(field_name))
    u = U[:,0]
    v = U[:,1]
    w = U[:,2]

    # Return the vector field components
    return u,v,w

def extract_plane_scalar_field(plane_data, field_name, verbose=False):
    """Extract the scalar field `field_name` in the plane `plane_data`"""

    # Put the scalar field field_name in array scalar
    scalar = npvtk.vtk_to_numpy(plane_data.GetPointData().GetArray(field_name))

    # Return the scalar field values extracted from the plane
    return  scalar
