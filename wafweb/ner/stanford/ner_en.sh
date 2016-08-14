#!/bin/sh
scriptdir=`dirname $0`
echo $scriptdir
#java -mx700m -cp "$scriptdir/stanford-ner.jar:$scriptdir/lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier $scriptdir/twitter_model_en.ser.gz -textFile $1 -outputFormat tsv > $2
