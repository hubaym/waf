#!/bin/sh
scriptdir=/Users/hubaymarton/Documents/errorfare/project/waf/env/wafweb/ner

java -mx700m -cp $scriptdir/trainfiles/*:$scriptdir/stanford/stanford-ner.jar:$scriptdir/stanford/lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier $scriptdir/commands/waf_twitter_model_en.ser.gz -textFile $1 -outputFormat tsv > $2
