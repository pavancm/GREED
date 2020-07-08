curl -L https://utexas.box.com/shared/static/0cufh9gy7yolzvhgpfs2s1kmh3h69xnu.yuv --output data/Flips_crf_0_120fps_1.yuv

curl -L https://utexas.box.com/shared/static/inpiicr4snicnlv7q34ddi1p4bghqm3z.yuv --output data/Flips_crf_0_120fps_2.yuv

curl -L https://utexas.box.com/shared/static/zf3qxb5bb9axfnalmq0nkm1d7m7q1d35.yuv --output data/Flips_crf_48_30fps.yuv

copy /b data/Flips_crf_0_120fps_1.yuv data/Flips_crf_0_120fps_2.yuv > data/Flips_crf_0_120fps.yuv
del data/Flips_crf_0_120fps_*
