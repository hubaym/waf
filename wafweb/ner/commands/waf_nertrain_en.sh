#!/bin/sh
scriptdir=/Users/hubaymarton/Documents/errorfare/project/waf/env/wafweb/ner
java -cp $scriptdir/trainfiles/*:$scriptdir/stanford/stanford-ner.jar:$scriptdir/stanford/lib/* edu.stanford.nlp.ie.crf.CRFClassifier -prop $scriptdir/properties/waf_trainfile_en.prop
