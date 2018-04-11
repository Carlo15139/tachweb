#!/usr/bin/env /bin/bash

if [ -f $virtualenv/bin/activate ]; then
    source $virtualenv/bin/activate
    pip3 install sphinx
    pip3 install sphinxcontrib-websupport 
    pip3 install -r $src_path/requirements.txt
    pip3 install -e $src_path

    rm -rf $doc_dir
    sphinx-build -c $virtualenv $src_path/docs/source $doc_dir
fi
