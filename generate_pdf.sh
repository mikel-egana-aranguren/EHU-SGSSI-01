#!/bin/sh

for dir in */
do 
    if [ $dir != "ShowerTemplate/" ] && [ $dir != "Conferencias/" ]
    then 
        proper_dir=${dir%/}
        m0=$(cat $PWD/$proper_dir/index.html.md5sum)
        m1=$(md5sum $PWD/$proper_dir/index.html  | cut -d' ' -f1)
        echo $m1 > $PWD/$proper_dir/index.html.md5sum
        if [ "$m0" != "$m1" ]; then
            shower pdf --cwd $PWD/$proper_dir -o $PWD/$proper_dir/index.pdf
        fi
    fi
done