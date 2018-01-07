from __future__ import print_function
import numpy as np
import tensorflow as tf
import sys
import argparse
import os
import time

from six.moves import cPickle
from utils import TextLoader
from model import Model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                        help='model directory to load stored checkpointed models from')
    parser.add_argument('-n', type=int, default=300,
                        help='number of words to sample')
    parser.add_argument('--prime', type=str, default=' ',
                        help='prime text')
    parser.add_argument('--pick', type=int, default=1,
                        help='1 = weighted pick, 2 = beam search pick')
    parser.add_argument('--width', type=int, default=4,
                        help='width of the beam search')
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)


def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

            result = model.sample(sess, words, vocab, args.n, args.prime, args.sample, args.pick, args.width)
            sys.stdout.write("{}\n".format(result))
            return result


def proc_main(main_word):
    # python sample.py --prime "KING RICHARD III:" -n 100 --pick 2 --width 4
    settings = {}
    settings['saver_dir'] = 'save'  # model directory to load stored checkpointed models from
    settings['n'] = 100  # number of words to sample
    settings['prime'] = main_word  # help='prime text
    settings['pick'] = 2  # 1 = weighted pick, 2 = beam search pick
    settings['width'] = 4  # width of the beam search')
    settings['sample'] = 1  # 0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces
    return proc_sample(settings)


def proc_sample(settings):
    with open(os.path.join(settings['save_dir'], 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(settings['save_dir'], 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(settings['save_dir'])
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

            result = model.sample(sess, words, vocab, settings['n'], settings['prime'], settings['sample'], settings['pick'],
                                  settings['width'])
            sys.stdout.write("{}\n".format(result))
            return result


if __name__ == '__main__':
    main()
