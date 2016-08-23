#!/bin/sh
#scriptdir=`dirname $0`
scriptdir="/Users/hubaymarton/Documents/errorfare/project/waf/env/wafweb/ner/stanford”
java -cp "$scriptdir/stanford-ner.jar:$scriptdir/lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop /Users/hubaymarton/Documents/errorfare/stanford-ner-2015-12-09/trainfile_en.prop
