# Driver to make the terrace profile plots
# FJC 01/11/17

# import modules
import matplotlib
matplotlib.use('Agg')
import sys
import os

import TerracePlotter

#=============================================================================
# This is the main function that runs the whole thing
#=============================================================================
def main(argv):

    # If there are no arguments, send to the welcome screen
    if not len(sys.argv) > 1:
        full_paramfile = print_welcome()
        sys.exit()

    # Get the arguments
    import argparse
    parser = argparse.ArgumentParser()

    # The location of the data files
    parser.add_argument("-dir", "--base_directory", type=str, help="The base directory with the terrace analysis. If this isn't defined I'll assume it's the same as the current directory.")
    parser.add_argument("-fname", "--fname_prefix", type=str, help="The prefix of your DEM WITHOUT EXTENSION!!! This must be supplied or you will get an error.")

    # Some filtering info for terrace pixels
    parser.add_argument("-min_size", "--min_size", type=int, help="The minimum size (in pixels) of a terrace patch. Default = 5", default=5)
    parser.add_argument("-min_elev", "--min_elev", type=int, help="The minimum elevation above the channel of a terrace pixel. Default = 0", default=0)
    parser.add_argument("-max_elev", "--max_elev", type=int, help="The maximum elevation above the channel of a terrace pixel. Default = large", default=10000000)

    # What sort of analyses you want to do
    parser.add_argument("-LP", "--long_profiler", type=bool, default=False, help="If this is true, I'll make plots of the terrace long profiles (Default = true)")
    parser.add_argument("-PR", "--plot_rasters", type=bool, default=False, help="If this is true, I'll make raster plots of the terrace locations (Default=false)")
    parser.add_argument("-HM", "--heat_map", type=bool, default=False, help="if true I'll make a heat map of terrace locations along the river long profile")
    parser.add_argument("-dips", "--dips", type=bool,default=False, help="If this is true, I'll calculate the dip and dip direction of each terrace.")
    parser.add_argument("-DT", "--digitised_terraces", type=bool,default=False, help="If this is true I'll filter the terrace points using a shapefile of digitised terraces.")
    parser.add_argument("-shp", "--shapefile_name", type=str, default=None, help="The shapefile of digitised terraces. Must be supplied if you want to filter terraces by shapefile, obvz.")

    # These control the format of your figures
    parser.add_argument("-fmt", "--FigFormat", type=str, default='png', help="Set the figure format for the plots. Default is png")
    parser.add_argument("-size", "--size_format", type=str, default='ESURF', help="Set the size format for the figure. Can be 'big' (16 inches wide), 'geomorphology' (6.25 inches wide), or 'ESURF' (4.92 inches wide) (defualt esurf).")

    args = parser.parse_args()

    # get the base directory
    if args.base_directory:
        this_dir = args.base_directory
        # check if you remembered a / at the end of your path_name
        if not this_dir.endswith("/"):
            print("You forgot the '/' at the end of the directory, appending...")
            this_dir = this_dir+"/"
    else:
        this_dir = os.getcwd()

    # check if you supplied the DEM prefix
    if not args.fname_prefix:
        print("WARNING! You haven't supplied your DEM name. Please specify this with the flag '-fname'")
        sys.exit()

    # print the arguments that you used to an output file for reproducibility
    with open(this_dir+args.fname_prefix+'_report.csv', 'w') as output:
        for arg in vars(args):
            output.write(str(arg)+','+str(getattr(args, arg))+'\n')
        output.close()

    # check if the slopes file exists
    filtered = this_dir+args.fname_prefix+'_terrace_info_filtered.csv'
    #if not os.path.isfile(filtered):
        # modify the terrace info file to filter some terraces.
    #    TerracePlotter.filter_terraces(this_dir, args.fname_prefix, args.min_size, args.min_elev, args.max_elev)

    if args.long_profiler:
        #if not args.digitised_terraces:
        TerracePlotter.long_profiler(this_dir, args.fname_prefix)
        #else:
            #TerracePlotter.long_profiler_dist(this_dir, args.fname_prefix, digitised_terraces=True, shapefile_name = args.shapefile_name)
            #TerracePlotter.long_profiler_centrelines(this_dir,args.fname_prefix,args.shapefile_name)

    # if args.plot_rasters:
    #     TerracePlotter.MakeRasterPlotTerraceIDs(this_dir, args.fname_prefix, args.FigFormat, args.size_format)
    #     TerracePlotter.MakeRasterPlotTerraceElev(this_dir, args.fname_prefix, args.FigFormat, args.size_format)
    if args.dips:
        TerracePlotter.write_dip_and_dipdir_to_csv(this_dir,args.fname_prefix, args.digitised_terraces, args.shapefile_name)
        # TerracePlotter.MakeRasterPlotTerraceDips(this_dir,args.fname_prefix,FigFormat=args.FigFormat,size_format=args.size_format)
    if args.heat_map:
        TerracePlotter.MakeTerraceHeatMap(this_dir, args.fname_prefix, prec=100, bw_method=0.03, FigFormat=args.FigFormat, ages="")

#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello! Welcome to the terrace long profiler tool.")
    print("You will need to tell me which directory to look in.")
    print("Use the -dir flag to define the working directory.")
    print("If you don't do this I will assume the data is in the same directory as this script.")
    print("For help type:")
    print("   python terrace_profile_plots.py -h\n")
    print("=======================================================================\n\n ")

#=============================================================================
if __name__ == "__main__":
    main(sys.argv[1:])
