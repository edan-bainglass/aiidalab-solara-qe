#!/usr/bin/env bash

for library in sssp pseudo-dojo; do
    for functional in PBE PBEsol; do
        if [ $library == "sssp" ]; then
            for accuracy in efficiency precision; do
                echo "Installing ${library} | ${accuracy} | ${functional}"
                aiida-pseudo install $library -x $functional -p $accuracy
            done
        else
            for accuracy in standard stringent; do
                for relativistic in SR FR; do
                    echo "Installing ${library} | ${accuracy} | ${relativistic} | ${functional}"
                    aiida-pseudo install $library -x $functional -p $accuracy -r $relativistic -f upf
                done
            done
        fi
    done
done
