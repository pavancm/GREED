#!/bin/bash
wget -L https://utexas.box.com/shared/static/0cufh9gy7yolzvhgpfs2s1kmh3h69xnu.yuv -O data/Flips_crf_0_120fps_1.yuv -q --show-progress

wget -L https://utexas.box.com/shared/static/inpiicr4snicnlv7q34ddi1p4bghqm3z.yuv -O data/Flips_crf_0_120fps_2.yuv -q --show-progress

wget -L https://utexas.box.com/shared/static/zf3qxb5bb9axfnalmq0nkm1d7m7q1d35.yuv -O data/Flips_crf_48_30fps.yuv -q --show-progress

cat data/Flips_crf_0_120fps_1.yuv data/Flips_crf_0_120fps_2.yuv > data/Flips_crf_0_120fps.yuv
rm -f data/Flips_crf_0_120fps_*
