#!/bin/bash

# Function to generate boxplot
generate_boxplot() {
    local datafile=$1
    local title=$2
    local xlabel=$3
    local ylabel=$4
    local outfile=$5

    # Check if gnuplot is installed
    if ! command -v gnuplot &> /dev/null; then
        echo "gnuplot could not be found. Please install it to generate the boxplot."
        return 1
    fi

    # Create a temporary gnuplot script
    local temp_gnuplot_script=$(mktemp)
    cat <<EOF > $temp_gnuplot_script
set term pngcairo enhanced font 'Verdana,10' size 640,480
set output '$outfile'
set title '$title'
unset key
set grid xtics ytics lt 1 lc rgb '#bbbbbb' lw 0.5 
set style fill solid border -1
set boxwidth 0.8
set style data boxes
plot '$datafile' u 2:4 w boxes title 'Boxplot'
EOF

    # Run gnuplot with the temporary script
    gnuplot $temp_gnuplot_script

    # Clean up the temporary script file
    rm -f $temp_gnuplot_script

    echo "Boxplot generated and saved as '$outfile'"
}

# Example usage
#datafile='data.dat'
#title='Sample Boxplot'
#xlabel='Categories'
#ylabel='Values'
#outfile='boxplot.png'

datafile=$1
title=$2
xlabel=$3
ylabel=$4
outfile=$5

# Call the generate_boxplot function with parameters
generate_boxplot "$datafile" "$title" "$xlabel" "$ylabel" "$outfile"
