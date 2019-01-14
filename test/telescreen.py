from watchdog.observers import Observer
from watchdog.events import *
import time
import os


class baseEvnetHandler(RegexMatchingEventHandler):
    # 修改次数
    check_count = 1

    def __init__(self):
        re_list = [
            r".*\.py$",
        ]
        super(baseEvnetHandler, self).__init__(re_list)

    def on_modified(self, event):
        # 清屏
        os.system("cls")

        print("\nmodified! {0}th changes".format(self.check_count))
        if event.is_directory:
            print("directory modified: {0}".format(event.src_path))
        else:
            print("file modified: {0}".format(event.src_path))

            # os.system("python ./single_test.py")
            # os.system("python ./lib_test/engine_core_test.py")
            os.system("python ./pipeline/pipeline_test.py")
            # os.system("python ./lib_test/Scraper/_test.py")

        self.check_count = self.check_count + 1


### test
if __name__ == "__main__":
    observer = Observer()
    event_handler = baseEvnetHandler()
    observer.schedule(event_handler, os.path.dirname(os.getcwd()), recursive=True)

    print("telescreen start")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
