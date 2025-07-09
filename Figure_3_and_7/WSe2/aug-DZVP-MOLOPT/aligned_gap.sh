grep 'G0W0 di' */cp2k.out | sed -E 's/(.*:)(.*)/\1\t\2/' | expand -t 40 | awk '{printf "%s%6s\n", substr($0, 1, length($0)-6), substr($0, length($0)-5)}'
