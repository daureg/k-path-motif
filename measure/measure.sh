# export PATH=$PATH:/d/devel/Octave3.6.2_gcc4.6.2/bin/
# from http://stackoverflow.com/a/3684051
# UNIX timestamp concatenated with nanoseconds
# rm -f answer timing
INST=$1
NAME=$(basename ${INST} '.txt')
echo $NAME
# python gold_miner.py $INST
# for i in {1..25}; do
# 	T="$(date +%s%N)"
# 	python fp.py < $INST >> answer
# 	# Time interval in nanoseconds
# 	T="$(($(date +%s%N)-T))"
# 	# Milliseconds (be more realistic)
# 	M="$((T/1000000))"
# 	echo "${M}" >> timing
# done
# python analyse.py
AVERAGE=$(tail -n 1 run.dat|cut -c2-)
# octave -qf histpdf.m
# cp hist-1.dat hist-${NAME}.dat
# cp pdf-1.dat pdf-${NAME}.dat
sed -e "s/AVERAGE/${AVERAGE}/g" norm.tex > ${NAME}.tex
sed -i "s/INSTANCE/${NAME}/g" ${NAME}.tex
pdflatex ${NAME}.tex
