import os
import glob
class Stopper:

    def __init__(self):
        return

    def build_stopped_corpus(self):
        cwd = os.getcwd()
        clean_cacm = os.path.join(cwd, 'clean_cacm')
        stopped_cacm = os.path.join(cwd, 'stopped_cacm')

        if not os.path.exists(clean_cacm):
            print "Clean corpus doesn't exist. It is created now. " \
                  "PLease put cleaned files inside the corpus folder"
            os.makedirs(clean_cacm, 0755)
            return
        if not os.path.exists(stopped_cacm):
            os.makedirs(stopped_cacm, 0755)

        stop_words = self.get_stop_words()
        os.chdir(clean_cacm)

        for eachfile in glob.glob('*.html'):
            content = open(eachfile).read()
            content = content.split()
            stopped_content = [x for x in content if x not in stop_words]
            final_content = " ".join(stopped_content)

            clean_file = open(os.path.join(stopped_cacm, eachfile), 'w')
            clean_file.write(final_content)
            clean_file.close()

    def get_stop_words(self):
        with open('common_words.txt') as f:
            stop_words = f.read().splitlines()

        return stop_words

def task3():
    s = Stopper()
    s.build_stopped_corpus()

task3()
