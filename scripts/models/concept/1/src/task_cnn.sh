source /home1/r/romap/neuralenv/nn/bin/activate
python /nlp/data/romap/law/task_2/scripts/cnn/concept/1/src/process_data.py /nlp/data/corpora/GoogleNews-vectors-negative300.bin concept 1
THEANO_FLAGS=mode=FAST_RUN,device=cpu,floatX=float32 python /nlp/data/romap/law/task_2/scripts/cnn/concept/1/src/conv_net_sentence.py -nonstatic -word2vec