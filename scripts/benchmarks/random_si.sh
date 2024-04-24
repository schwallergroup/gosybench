

# Select 20 random files from ../../data/ and open the file si_0.pdf

files=($(ls ../../notebooks/data/ | shuf -n 20))
for file in ${files[@]}; do
    echo "Opening file $file"
    open ../../notebooks/data/$file/si_0.pdf
done