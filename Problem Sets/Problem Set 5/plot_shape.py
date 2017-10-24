def plot_shape(map_info, map, facecolor, edgecolor,
               linewidths, zorder, transparancy):

    '''
    This function plots elements of shapefiles already read into python using
    map.readshapefile() with the necessary arguements.

    Input:
        map_info and map: indicate the names assigned to the previously read
                          shapefiles.

        remaining arguements which will be passed to ax.add_collection

    Output:
        plots elements of the shapefiles in the active matplotlib plot

    '''

    n, n2, fc, ec, lw, z, transp = (map_info, map, facecolor, edgecolor,
                                    linewidths, zorder, transparancy)
    patches = []

    for info, shape in zip(n, n2):
        patches.append(Polygon(np.array(shape), True))

        ax.add_collection(PatchCollection(patches, facecolor=fc,
                                          edgecolor=ec, linewidths=lw,
                                          zorder=z, alpha=transp))
