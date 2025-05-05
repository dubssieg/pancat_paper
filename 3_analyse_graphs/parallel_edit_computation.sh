# Print timestamp before running the command
echo "Start time: $(date)"
# Run the command
while read file;
do
    echo "Comparing "$file
    /usr/bin/time -v ./rs-pancat-compare "mc/"$file "pggb/"$file > /dev/null 2> "time_"${file::-4}".txt" &
done < list.txt
# Wait for all the background processes to finish
wait
# Print timestamp after running the command
echo "End time: $(date)"


# Start time: Wed  5 Mar 16:10:22 CET 2025
# End time: Wed  5 Mar 16:33:40 CET 2025
# Peak memory usage: 20.3 Gb