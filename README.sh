# Delete bogus gene model(s) from r1.2
for model in 02024
do
    cat pdom-annot-r1.2.gff3 \
        | grep -v PdomGENEr1.2-${model} \
        | grep -v PdomMRNAr1.2-${model} \
        > pdom-annot-r1.2-without-deleted.gff3
done

# Clean up accepted yrGATE annotations
# perl yrgate-to-gff3.pl --passwd=${SECRET} > yrgate-accepted-as-of-2015_11_09.gff3
# [CanonGFF3] AEGeAn Toolkit v0.14.0 (unstable d6b011688a)
canon-gff3 --source yrGATE yrgate-accepted-as-of-2015_11_09.gff3 2> >(grep -v 'has not been previously introduced' | grep -v 'does not begin with') \
    | gt gff3 -sort -tidy \
    | grep -v $'\tintron\t' \
    | python yrgate-prep.py - \
    > pdom-annot-yrgate.gff3

# Remove r1.2 annotations overlapping with yrGATE annotations
python intersect-v.py pdom-annot-r1.2-without-deleted.gff3 \
                      pdom-annot-yrgate.gff3 \
    > pdom-annot-r1.2-without-yrgate-repl.gff3

# Create the new annotation r1.3
gt gff3 -sort -tidy pdom-annot-r1.2-without-yrgate-repl.gff3 \
                    pdom-annot-yrgate.gff3 \
    > pdom-annot-r1.3.gff3
